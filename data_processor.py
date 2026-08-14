"""
Insight Flow — Data Processor Module
Handles CSV upload validation, parsing, column detection, and metadata extraction.
"""
import pandas as pd
import numpy as np

class DataValidationError(Exception):
    pass

class DataProcessor:
    DATE_PATTERNS = ['date','datetime','time','timestamp','created','updated',
        'order_date','purchase_date','transaction_date','sale_date','period','month','year']

    def __init__(self):
        self.df = None
        self.metadata = {}
        self.date_columns = []
        self.numeric_columns = []
        self.categorical_columns = []
        self.primary_date_col = None

    def validate_and_load(self, uploaded_file):
        if uploaded_file.size == 0:
            raise DataValidationError("The uploaded file is empty.")
        try:
            uploaded_file.seek(0)
            self.df = pd.read_csv(uploaded_file)
        except Exception as e:
            raise DataValidationError(f"Unable to parse CSV. Details: {e}")

        if self.df.empty or len(self.df.columns) < 2:
            raise DataValidationError("Dataset must contain at least two columns with data rows.")

        self._detect_date_columns()
        self._detect_numeric_columns()
        self._detect_categorical_columns()

        if not self.date_columns:
            raise DataValidationError("Dataset does not contain valid date fields.")
        if not self.numeric_columns:
            raise DataValidationError("CSV contains insufficient numerical metrics.")

        self.primary_date_col = self.date_columns[0]
        self.df[self.primary_date_col] = pd.to_datetime(self.df[self.primary_date_col], errors='coerce')
        self.df = self.df.dropna(subset=[self.primary_date_col])
        if len(self.df) == 0:
            raise DataValidationError("All date values could not be parsed.")
        self.df = self.df.sort_values(by=self.primary_date_col).reset_index(drop=True)
        for col in self.numeric_columns:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        self._extract_metadata()
        return self.df

    def _detect_date_columns(self):
        self.date_columns = []
        for col in self.df.columns:
            cl = col.lower().strip()
            if self.df[col].dtype == 'datetime64[ns]':
                self.date_columns.append(col); continue
            name_match = any(p in cl for p in self.DATE_PATTERNS)
            if name_match or self.df[col].dtype == 'object':
                try:
                    parsed = pd.to_datetime(self.df[col], errors='coerce')
                    if parsed.notna().sum() / len(self.df) > 0.5:
                        self.date_columns.append(col)
                except: pass

    def _detect_numeric_columns(self):
        self.numeric_columns = []
        for col in self.df.columns:
            if col in self.date_columns: continue
            if pd.api.types.is_numeric_dtype(self.df[col]):
                self.numeric_columns.append(col)
            else:
                try:
                    c = pd.to_numeric(self.df[col], errors='coerce')
                    if c.notna().sum() / len(self.df) > 0.6:
                        self.numeric_columns.append(col)
                except: pass

    def _detect_categorical_columns(self):
        self.categorical_columns = []
        for col in self.df.columns:
            if col in self.date_columns or col in self.numeric_columns: continue
            
            if self.df[col].nunique() / len(self.df) < 0.5 and self.df[col].nunique() <= 200:
                self.categorical_columns.append(col)

    def _extract_metadata(self):
        dmin = self.df[self.primary_date_col].min()
        dmax = self.df[self.primary_date_col].max()
        self.metadata = {
            'total_rows': len(self.df), 'total_columns': len(self.df.columns),
            'column_names': list(self.df.columns),
            'date_columns': self.date_columns, 'numeric_columns': self.numeric_columns,
            'categorical_columns': self.categorical_columns,
            'primary_date_column': self.primary_date_col,
            'date_range_start': dmin.strftime('%Y-%m-%d') if pd.notna(dmin) else 'N/A',
            'date_range_end': dmax.strftime('%Y-%m-%d') if pd.notna(dmax) else 'N/A',
            'date_span_days': (dmax - dmin).days if pd.notna(dmin) and pd.notna(dmax) else 0,
            'categories': {col: self.df[col].dropna().unique().tolist()[:50] for col in self.categorical_columns},
            'metric_ranges': {col: {'min': float(self.df[col].min()), 'max': float(self.df[col].max()),
                'mean': round(float(self.df[col].mean()),2)} for col in self.numeric_columns if pd.notna(self.df[col].min())}
        }

    def get_filtered_data(self, df, date_col, start_date, end_date):
        mask = (df[date_col] >= pd.Timestamp(start_date)) & (df[date_col] <= pd.Timestamp(end_date))
        return df.loc[mask].copy()

    def get_metadata(self):
        return self.metadata
