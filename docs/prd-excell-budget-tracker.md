# Task Execution Plan
## Excel Budget Generator Development

**Project:** Python Excel Budget Generator  
**Version:** 1.0.0  
**Start Date:** 2025-10-15  
**Target Completion:** 8 weeks  

---

## Task Organization System

### Priority Levels
- 🔴 **P0**: Critical path, blocking
- 🟠 **P1**: High priority, required for v1.0
- 🟡 **P2**: Medium priority, nice to have
- 🟢 **P3**: Low priority, future enhancement

### Status Indicators
- ⬜ Not Started
- 🟦 In Progress
- 🟨 Blocked
- ✅ Complete
- ❌ Cancelled

---

## PHASE 1: Foundation & Setup (Week 1-2)

### 1.1 Project Initialization
**Priority:** 🔴 P0 | **Status:** ✅ | **Owner:** Dev Lead | **Est:** 4h

#### Tasks:
- [ ] Install `uv` package manager
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- [x] Create project directory structure
  ```bash
  mkdir -p excel-budget-generator/{src/budget_generator/{sheets,formatting,formulas,utils},tests/{test_sheets,test_formatting,fixtures},examples}
  ```
- [ ] Initialize project with `uv init`
- [x] Create `pyproject.toml` with project metadata
- [x] Set up `.gitignore` for Python projects
- [ ] Initialize git repository
- [x] Create README.md skeleton

**Deliverable:** Project structure ready for development

**Dependencies:** None

**Verification:**
```bash
uv sync
tree excel-budget-generator/
```

---

### 1.2 Dependency Configuration
**Priority:** 🔴 P0 | **Status:** ✅ | **Owner:** Dev Lead | **Est:** 2h

#### Tasks:
- [x] Add core dependencies to `pyproject.toml`:
  ```toml
  dependencies = [
      "openpyxl>=3.1.0",
      "click>=8.1.0",
  ]
  ```
- [x] Add development dependencies:
  ```toml
  [project.optional-dependencies]
  dev = [
      "pytest>=7.4.0",
      "pytest-cov>=4.1.0",
      "black>=23.0.0",
      "ruff>=0.1.0",
      "mypy>=1.5.0",
  ]
  ```
- [x] Configure project entry point in `pyproject.toml`
- [x] Run `uv sync` to create virtual environment
- [x] Run `uv sync --extra dev` to install dev dependencies
- [x] Verify installations with `uv pip list`

**Deliverable:** All dependencies installed and locked

**Dependencies:** 1.1

**Verification:**
```bash
uv run python -c "import openpyxl; print(openpyxl.__version__)"
uv run pytest --version
```

---

### 1.3 JSON Loader Module
**Priority:** 🔴 P0 | **Status:** ✅ | **Owner:** Backend Dev | **Est:** 6h

#### Tasks:
- [x] Create `src/budget_generator/utils/json_loader.py`
- [x] Implement `load_json_spec(filepath: Path) -> dict`
  - Read JSON file
  - Parse into dictionary
  - Handle file not found errors
  - Handle JSON parse errors
- [x] Implement `validate_json_structure(spec: dict) -> bool`
  - Check required top-level keys (meta, workbook, sheets)
  - Validate sheet names match specification
  - Check named_ranges structure
  - Return detailed error messages
- [x] Add type hints for all functions
- [x] Add comprehensive docstrings
- [x] Create `tests/test_json_loader.py`
- [x] Write unit tests for happy path
- [x] Write unit tests for error cases
- [x] Create test fixture: `tests/fixtures/valid_spec.json`
- [x] Create test fixture: `tests/fixtures/invalid_spec.json`

**Deliverable:** JSON loader with validation and tests

**Dependencies:** 1.2

**Verification:**
```bash
uv run pytest tests/test_json_loader.py -v
```

**Code Template:**
```python
from pathlib import Path
import json
from typing import Dict, Any

def load_json_spec(filepath: Path) -> Dict[str, Any]:
    """Load and parse JSON specification file.
    
    Args:
        filepath: Path to JSON specification file
        
    Returns:
        Parsed JSON as dictionary
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
```

---

### 1.4 CLI Framework Setup
**Priority:** 🔴 P0 | **Status:** ✅ | **Owner:** Backend Dev | **Est:** 4h

#### Tasks:
- [x] Create `src/budget_generator/__main__.py`
- [x] Set up Click CLI group
- [x] Implement `generate` command with arguments:
  - `json_file` (required): Path to JSON spec
  - `--output, -o`: Output Excel file path
  - `--verbose, -v`: Enable verbose logging
  - `--validate-only`: Validate without generating
  - `--version`: Show version
- [x] Add logging configuration
- [x] Implement error handling and user-friendly messages
- [x] Create `tests/test_cli.py`
- [x] Test CLI argument parsing
- [x] Test error messages

**Deliverable:** Working CLI that accepts arguments

**Dependencies:** 1.3

**Verification:**
```bash
uv run budget-generator --help
uv run budget-generator generate --help
uv run budget-generator --version
```

**Code Template:**
```python
import click
import logging
from pathlib import Path

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Excel Budget Generator - Create budget workbooks from JSON."""
    pass

@cli.command()
@click.argument('json_file', type=click.Path(exists=True, path_type=Path))
@click.option('--output', '-o', type=click.Path(path_type=Path), 
              default='budget_workbook.xlsx', help='Output Excel file path')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--validate-only', is_flag=True, 
              help='Validate JSON without generating file')
def generate(json_file, output, verbose, validate_only):
    """Generate Excel budget workbook from JSON specification."""
    # Implementation here
    pass

def main():
    cli()

if __name__ == '__main__':
    main()
```

---

### 1.5 Basic Workbook Creator
**Priority:** 🔴 P0 | **Status:** ✅ | **Owner:** Backend Dev | **Est:** 4h

#### Tasks:
- [x] Create `src/budget_generator/generator.py`
- [x] Implement `BudgetGenerator` class
- [x] Implement `create_workbook() -> Workbook`
- [x] Implement `create_sheets(spec: dict)`
  - Create all 6 sheets with correct names
  - Set sheet visibility (hide Calculations, Dropdown Data)
- [x] Implement `save_workbook(output_path: Path)`
- [x] Add error handling for file write permissions
- [x] Create `tests/test_generator.py`
- [x] Test workbook creation
- [x] Test sheet creation with correct names/visibility
- [x] Test file saving

**Deliverable:** Basic workbook generator that creates empty sheets

**Dependencies:** 1.2

**Verification:**
```bash
uv run python -c "from budget_generator.generator import BudgetGenerator; gen = BudgetGenerator({}); gen.create_workbook(); gen.save_workbook('test.xlsx')"
# Open test.xlsx and verify 6 sheets exist
```

**Code Template:**
```python
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from pathlib import Path
from typing import Dict, Any

class BudgetGenerator:
    """Generate Excel budget workbooks from JSON specifications."""
    
    def __init__(self, spec: Dict[str, Any]):
        self.spec = spec
        self.workbook: Workbook = None
        
    def create_workbook(self) -> Workbook:
        """Create new Excel workbook."""
        self.workbook = Workbook()
        # Remove default sheet
        if 'Sheet' in self.workbook.sheetnames:
            del self.workbook['Sheet']
        return self.workbook
    
    def create_sheets(self):
        """Create all worksheets per specification."""
        sheets_spec = self.spec['workbook']['sheets']
        for sheet_info in sheets_spec:
            ws = self.workbook.create_sheet(sheet_info['name'])
            if sheet_info['visibility'] == 'hidden':
                ws.sheet_state = 'hidden'
```

---

### 1.6 Settings Sheet Implementation
**Priority:** 🟠 P1 | **Status:** ✅ | **Owner:** Backend Dev | **Est:** 6h

#### Tasks:
- [x] Create `src/budget_generator/sheets/settings.py`
- [x] Implement `build_settings_sheet(ws: Worksheet, spec: dict)`
- [x] Create merged header cell (B2:E2) with "General Settings"
- [x] Apply header formatting (bold, green fill #D9EAD3, center align)
- [x] Add Starting Year label (B4) and value (C4)
- [x] Add helper text (D4)
- [x] Add Late Income Enabled label (B6) and dropdown (C6)
- [x] Add Late Income Day label (B7) and value (C7)
- [x] Apply data validation to C6 (TRUE/FALSE list)
- [x] Apply data validation to C7 (whole number 1-31)
- [x] Apply border to header section (B2:E2, bottom border)
- [x] Create `src/budget_generator/formatting/styles.py`
- [x] Implement `apply_fill(cell, hex_color)`
- [x] Implement `merge_and_format(ws, range, **kwargs)`
- [x] Create `src/budget_generator/formatting/validation.py`
- [x] Implement `add_list_validation(ws, range, options)`
- [x] Implement `add_number_validation(ws, range, min, max)`
- [x] Create `tests/test_sheets/test_settings.py`
- [x] Test all cell values
- [x] Test formatting
- [x] Test data validation rules

**Deliverable:** Fully functional Settings sheet

**Dependencies:** 1.5

**Verification:**
```python
# Generate workbook with Settings sheet
# Open in Excel and verify:
# - Header is merged and formatted
# - Dropdowns work
# - Validation prevents invalid input
```

**Code Template:**
```python
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.worksheet.datavalidation import DataValidation

def build_settings_sheet(ws: Worksheet, spec: dict):
    """Build Settings worksheet according to specification."""
    layout = spec['layout']
    
    # Header
    ws.merge_cells('B2:E2')
    header_cell = ws['B2']
    header_cell.value = "General Settings"
    header_cell.font = Font(bold=True)
    header_cell.fill = PatternFill(start_color="D9EAD3", fill_type="solid")
    header_cell.alignment = Alignment(horizontal="center")
    
    # Starting Year
    ws['B4'] = "Starting Year"
    ws['C4'] = 2025
    ws['D4'] = "← Change this to your budget base year"
    
    # Late Income controls
    ws['B6'] = "Late Monthly Income Enabled"
    ws['C6'] = "FALSE"
    
    dv = DataValidation(type="list", formula1='"TRUE,FALSE"')
    ws.add_data_validation(dv)
    dv.add(ws['C6'])
```

---

## PHASE 2: Core Sheets (Week 3-4)

### 2.1 Dropdown Data Sheet
**Priority:** 🔴 P0 | **Status:** ✅ | **Owner:** Backend Dev | **Est:** 4h

#### Tasks:
- [x] Create `src/budget_generator/sheets/dropdown.py`
- [x] Implement `build_dropdown_sheet(ws: Worksheet, spec: dict)`
- [x] Add header row (B2:C2) with "Years" and "Months"
- [x] Apply header formatting (purple fill #D9D2E9, bold)
- [x] Generate Years formulas (B3:B7):
  - `=StartingYear+0` through `=StartingYear+4`
- [x] Add month abbreviations (C3:C14): Jan, Feb, Mar, etc.
- [x] Create `src/budget_generator/formulas/builder.py`
- [x] Implement `build_year_formula(offset: int) -> str`
- [x] Create tests for dropdown sheet
- [x] Verify formulas are correct
- [x] Verify values populate correctly

**Deliverable:** Dropdown Data sheet with dynamic year list

**Dependencies:** 1.6

**Verification:**
```python
# Change StartingYear in Settings
# Verify Years list updates automatically
```

---

### 2.2 Named Ranges Setup
**Priority:** 🔴 P0 | **Status:** ✅ | **Owner:** Backend Dev | **Est:** 6h

#### Tasks:
- [x] Create `src/budget_generator/utils/named_ranges.py`
- [x] Implement `create_named_range(workbook, name, sheet_name, cell_range)`
- [x] Implement `NamedRangeManager` class to handle all ranges
- [ ] Create Settings ranges:
  - StartingYear → Settings!E8
  - LateIncomeEnabled → Settings!J16
  - LateIncomeDay → Settings!E18
- [ ] Create Dropdown Data ranges:
  - YearsList → 'Dropdown Data'!B3:B7
  - MonthsList → 'Dropdown Data'!C3:C14
- [ ] Create placeholder ranges for Planning sheet (TBD):
  - IncomeCats, ExpenseCats, SavingsCats
  - IncomeGrid, ExpenseGrid, SavingsGrid
  - IncomeTotals, ExpenseTotals, SavingsTotals
- [ ] Create Dashboard ranges:
  - DashYear → 'Budget Dashboard'!C3
  - DashPeriod → 'Budget Dashboard'!C4
- [x] Handle scoped vs workbook-level ranges
- [x] Add error handling for duplicate ranges
- [x] Create tests for named range creation
- [ ] Verify ranges are accessible in Excel

**Deliverable:** Named range management system

**Dependencies:** 2.1

**Verification:**
```excel
# In Excel: Formulas → Name Manager
# Verify all ranges exist with correct references
# Test: =StartingYear in any cell should resolve
```

**Code Template:**
```python
from openpyxl import Workbook
from openpyxl.workbook.defined_name import DefinedName

class NamedRangeManager:
    """Manage workbook-level named ranges."""
    
    def __init__(self, workbook: Workbook):
        self.workbook = workbook
        
    def create_range(self, name: str, sheet_name: str, 
                     cell_range: str, scope: str = 'workbook'):
        """Create a named range.
        
        Args:
            name: Range name (e.g., 'StartingYear')
            sheet_name: Worksheet name
            cell_range: Cell reference (e.g., 'C4' or 'B3:B7')
            scope: 'workbook' or 'sheet'
        """
        # Ensure sheet name is properly quoted if it contains spaces
        sheet_ref = f"'{sheet_name}'" if ' ' in sheet_name else sheet_name
        formula = f"{sheet_ref}!${cell_range.replace(':', '$').replace('$', '', 1)}"
        
        defined_name = DefinedName(name, attr_text=formula)
        self.workbook.defined_names.append(defined_name)
```

---

### 2.3 Budget-Planning Sheet - Structure
**Priority:** 🔴 P0 | **Status:** ✅ | **Owner:** Backend Dev | **Est:** 8h

#### Tasks:
- [x] Create `src/budget_generator/sheets/planning.py`
- [x] Implement `build_planning_sheet(ws: Worksheet, spec: dict)`
- [x] Create year banner (E5:Q5):
  - Merge cells
  - Formula: `=StartingYear+0`
  - Format: bold, blue fill #CFE2F3, center
- [x] Create month header row (E6:Q6):
  - Formulas: `=IF(E7=0,"Jan ✓","Jan")` … `=IF(Q7=0,"Total ✓","Total")`
  - Format: bold, blue fill #DAE3F3, center
- [x] Implement freeze panes at E12
- [x] Create section builder helper function
- [x] Build Income section (rows 10-24):
  - Title cell (D10) with "Income" and green fill #43D40F
  - Category column (D12:D23): Salary, Freelance, Investments, Other, [blanks to row 23]
  - Data grid (E12:Q23): initialize to 0 with row totals in column Q
  - Total row label (D24): "Total Income"
  - Total formulas (E24:Q24): SUM each column
  - Format: yellow fill #FFF2CC for totals
  - Box with borders
- [x] Build Expenses section (rows 31-45):
  - Title cell (D31) with "Expenses" and red fill #F01010
  - Category column (D33:D44): 10 expense categories + blanks
  - Data grid (E33:Q44): initialize to 0
  - Total row label (D45): "Total Expenses"
  - Apply borders and totals formatting
- [x] Build Savings section (rows 53-67):
  - Title cell (D53) with "Savings" and blue fill #1564ED
  - Category column (D55:D66): savings categories + blanks
  - Data grid (E55:Q66): initialize to 0
  - Total row label (D67): "Total Savings"
  - Apply borders and totals formatting
- [x] Create tests for planning sheet structure

**Deliverable:** Budget-Planning sheet with all three sections

**Dependencies:** 2.2

**Verification:**
```python
# Verify all sections exist
# Verify formulas calculate totals
# Verify formatting matches spec
```

---

### 2.4 Budget-Planning Sheet - Formulas & Formatting
**Priority:** 🔴 P0 | **Status:** ✅ | **Owner:** Backend Dev | **Est:** 6h

- [x] Implement total formulas for all sections
- [x] Use formula builder to generate SUM formulas dynamically
- [x] Create Unallocated row (D7, E7:Q7):
  - Label: "Unallocated (per month)"
  - Formula: `=E24-E45-E67` (for each month column)
- [x] Create `src/budget_generator/formatting/conditional.py`
- [x] Implement `add_conditional_format(ws, range, rule_type, **kwargs)`
- [x] Add conditional formatting to Unallocated row:
  - Green (#B6D7A8) when = 0
  - Red (#F4CCCC) when < 0
  - Gray (#D9D9D9) when all sections = 0 (custom formula)
- [x] Update named ranges for Planning sheet:
  - IncomeCats → 'Budget-Planning'!D12:D23
  - ExpenseCats → 'Budget-Planning'!D33:D44
  - SavingsCats → 'Budget-Planning'!D55:D66
  - IncomeGrid → 'Budget-Planning'!E12:Q23
  - IncomeHeader → 'Budget-Planning'!D10
  - IncomeTotals → 'Budget-Planning'!E24:Q24
  - (similar for Expenses and Savings)
- [x] Apply number formatting (accounting format) to data cells
- [x] Create tests for formulas
- [x] Create tests for conditional formatting

**Deliverable:** Fully functional Budget-Planning sheet for Year 1

**Dependencies:** 2.3

**Verification:**
```python
# Enter budget values
# Verify totals calculate correctly
# Verify Unallocated shows correct colors
# Change StartingYear, verify banner updates
```

**Code Template:**
```python
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import PatternFill

def add_unallocated_conditional_formatting(ws, start_col, end_col, row):
    """Add conditional formatting to Unallocated row."""
    range_str = f"{start_col}{row}:{end_col}{row}"
    
    # Rule 1: Green when equals 0
    green_fill = PatternFill(start_color="B6D7A8", fill_type="solid")
    rule1 = CellIsRule(operator='equal', formula=['0'], fill=green_fill)
    
    # Rule 2: Red when less than 0
    red_fill = PatternFill(start_color="F4CCCC", fill_type="solid")
    rule2 = CellIsRule(operator='lessThan', formula=['0'], fill=red_fill)
    
    # Rule 3: Gray when all zero (custom formula)
    gray_fill = PatternFill(start_color="D9D9D9", fill_type="solid")
    rule3 = FormulaRule(formula=[f'AND({start_col}13=0,{start_col}26=0,{start_col}34=0)'], 
                        fill=gray_fill)
    
    ws.conditional_formatting.add(range_str, rule1)
    ws.conditional_formatting.add(range_str, rule2)
    ws.conditional_formatting.add(range_str, rule3)
```

---

### 2.5 Budget-Planning Sheet - Year 2 Scaffold
**Priority:** 🟠 P1 | **Status:** ✅ | **Owner:** Backend Dev | **Est:** 4h

- [x] Implement Year 2 banner (S5:AD5):
  - Formula: `=StartingYear+1`
- [x] Create Year 2 month headers (S6:AD6) using the same `IF` formulas as Year 1
- [x] Add note/comment about extending sections manually
- [x] Optionally: implement loop to create multiple years from spec
- [x] Update documentation about multi-year support
- [x] Create tests

**Deliverable:** Year 2 header structure in Budget-Planning sheet

**Dependencies:** 2.4

---

### 2.6 Budget Tracking Sheet - Table Setup
**Priority:** 🔴 P0 | **Status:** ✅ | **Owner:** Backend Dev | **Est:** 6h

#### Tasks:
- [x] Create `src/budget_generator/sheets/tracking.py`
- [x] Implement `build_tracking_sheet(ws: Worksheet, spec: dict)`
- [x] Create Excel Table "tblTracking" (B2:H1002)
- [x] Set table headers:
  - Date, Type, Category, Amount, Details, Balance, Effective Date
- [x] Apply table style (medium or light blue)
- [x] Disable table filter buttons
- [x] Add header formatting (bold, blue fill)
- [x] Set column widths appropriately
- [x] Create tests for table structure

**Deliverable:** Tracking sheet with table structure

**Dependencies:** 2.2

**Verification:**
```python
# Verify table exists with correct name
# Verify headers are correct
# Verify table extends to row 1002
```

**Code Template:**
```python
from openpyxl.worksheet.table import Table, TableStyleInfo

def build_tracking_sheet(ws: Worksheet, spec: dict):
    """Build Budget Tracking worksheet."""
    # Add headers
    headers = ["Date", "Type", "Category", "Amount", "Details", "Balance", "Effective Date"]
    for idx, header in enumerate(headers, start=2):  # Start at column B
        cell = ws.cell(row=2, column=idx)
        cell.value = header
    
    # Create table
    tab = Table(displayName="tblTracking", ref="B2:H1002")
    style = TableStyleInfo(name="TableStyleMedium2", 
                          showFirstColumn=False,
                          showLastColumn=False, 
                          showRowStripes=True, 
                          showColumnStripes=False)
    tab.tableStyleInfo = style
    ws.add_table(tab)
```

---

### 2.7 Budget Tracking Sheet - Data Validation
**Priority:** 🔴 P0 | **Status:** ✅ | **Owner:** Backend Dev | **Est:** 6h

#### Tasks:
- [x] Add date validation to Date column (B3:B1002):
  - Type: date
  - Operator: between
  - Formula1: 1/1/2000
  - Formula2: 12/31/2100
- [x] Add list validation to Type column (C3:C1002):
  - Source: "Income,Expense,Saving"
- [x] Add dynamic list validation to Category column (D3:D1002):
  - Formula: `=IF($C3="Income",IncomeCats,IF($C3="Expense",ExpenseCats,SavingsCats))`
  - Note: This is row-dependent, must apply to each row
- [x] Implement helper function to apply validation to ranges
- [x] Handle special case of row-dependent validation
- [x] Create tests for validation rules

**Deliverable:** Tracking sheet with all data validation

**Dependencies:** 2.6

**Verification:**
```excel
# In Excel:
# - Try entering invalid date → should reject
# - Try entering invalid Type → should reject
# - Select Type=Income, verify Category dropdown shows income categories
# - Select Type=Expense, verify Category dropdown shows expense categories
```

**Code Template:**
```python
from openpyxl.worksheet.datavalidation import DataValidation

def add_tracking_validations(ws, named_ranges_exist=True):
    """Add data validation rules to tracking sheet."""
    # Date validation
    date_dv = DataValidation(type="date", operator="between",
                            formula1="1/1/2000", formula2="12/31/2100")
    ws.add_data_validation(date_dv)
    date_dv.add("B3:B1002")
    
    # Type validation
    type_dv = DataValidation(type="list", formula1='"Income,Expense,Saving"')
    ws.add_data_validation(type_dv)
    type_dv.add("C3:C1002")
    
    # Category validation (dynamic based on Type)
    # Note: Row-dependent formulas require special handling
    for row in range(3, 1003):
        cat_dv = DataValidation(type="list", 
                               formula1=f'=IF($C{row}="Income",IncomeCats,'
                                       f'IF($C{row}="Expense",ExpenseCats,SavingsCats))')
        ws.add_data_validation(cat_dv)
        cat_dv.add(f"D{row}")
```

---

### 2.8 Budget Tracking Sheet - Formulas & Formatting
**Priority:** 🔴 P0 | **Status:** ✅ | **Owner:** Backend Dev | **Est:** 8h

#### Tasks:
- [x] Implement Balance column formula (G3:G1002):
  ```excel
  =SUMPRODUCT((tblTracking[Date]<=[@Date])*(tblTracking[Type]="Income")*tblTracking[Amount])
  -SUMPRODUCT((tblTracking[Date]<=[@Date])*((tblTracking[Type]="Expense")+(tblTracking[Type]="Saving"))*tblTracking[Amount])
  ```
- [ ] Note: Use structured table references ([@Date], tblTracking[Date])
- [x] Implement Effective Date column formula (H3:H1002):
  ```excel
  =IF(AND(LateIncomeEnabled,[@Type]="Income",DAY([@Date])>LateIncomeDay),
     DATE(YEAR([@Date]),MONTH([@Date])+1,1),[@Date])
  ```
- [x] Apply number format to Effective Date: "yyyy-mm-dd"
- [x] Apply accounting number format to Amount column
- [x] Add conditional formatting:
  - Orange fill (#FCE5CD) to Category column when contains "#N/A"
  - Green fill (#D9EAD3) to Amount column when Type="Income"
- [x] Create formula builder helpers for SUMPRODUCT
- [x] Create tests for formulas with sample data
- [x] Test late income calculation logic

**Deliverable:** Fully functional Tracking sheet with formulas

**Dependencies:** 2.7

**Verification:**
```python
# Add test transactions
# Verify Balance calculates correctly
# Verify Effective Date shifts late income to next month
# Test with LateIncomeEnabled=TRUE and FALSE
```

---

## PHASE 3: Advanced Features (Week 5-6)

### 3.1 Calculations Sheet - Metrics Tiles
**Priority:** 🟠 P1 | **Status:** ✅ | **Owner:** Backend Dev | **Est:** 6h

#### Tasks:
- [x] Create `src/budget_generator/sheets/calculations.py`
- [x] Implement `build_calculations_sheet(ws: Worksheet, spec: dict)`
- [x] Create header row (B2:D2):
  - Values: "Metric", "Value", "Notes"
  - Format: purple fill #EAD1DC, bold
- [x] Create metric rows (B3:D6):
  - Row 3: "Current Date" | `=TODAY()` | ""
  - Row 4: "Last Record Date" | `=MAX(tblTracking[Date])` | ""
  - Row 5: "Number of Records" | `=COUNTA(tblTracking[Date])` | ""
  - Row 6: "Tracking Balance" | `=IFERROR(LOOKUP(2,1/(tblTracking[Date]<>""),tblTracking[Balance]),0)` | ""
- [x] Apply borders to tile section
- [x] Create tests

**Deliverable:** Calculations sheet with metric tiles

**Dependencies:** 2.8

**Verification:**
```python
# Add tracking data
# Verify metrics update correctly
# Verify LOOKUP formula gets latest balance
```

---

### 3.2 Calculations Sheet - Helper Tables
**Priority:** 🔴 P0 | **Status:** ✅ | **Owner:** Backend Dev | **Est:** 4h

#### Tasks:
- [x] Create MonthMap table (J2:K13):
  - Column J: Jan, Feb, Mar, ..., Dec
  - Column K: 1, 2, 3, ..., 12
- [x] Create named range: MonthMap → Calculations!J2:K13
- [x] Create MonthIdx cell (K1):
  - Formula: `=INDEX(INDEX(MonthMap,0,2),MATCH(DashPeriod,INDEX(MonthMap,0,1),0))`
- [x] Create named range: MonthIdx → Calculations!K1
- [x] Create tests for month index lookup

**Deliverable:** Month mapping helper for dashboard

**Dependencies:** 3.1

**Verification:**
```python
# Set DashPeriod to different months
# Verify MonthIdx resolves to correct number
```

---

### 3.3 Calculations Sheet - Budget vs Tracked Table
**Priority:** 🔴 P0 | **Status:** ✅ | **Owner:** Backend Dev | **Est:** 8h

#### Tasks:
- [x] Create comparison table header (E2:H2):
  - Values: "Section", "BudgetedMonth", "TrackedMonth", "Remaining"
  - Format: blue fill #DEEAF6, bold
- [x] Create Income row (E3:H3):
  - E3: "Income"
  - F3: `=CHOOSE(MonthIdx,D13,E13,F13,G13,H13,I13,J13,K13,L13,M13,N13,O13)`
  - G3: `=SUMPRODUCT((MONTH(tblTracking[Effective Date])=MonthIdx)*(tblTracking[Type]="Income")*tblTracking[Amount])`
  - H3: `=F3-G3`
- [x] Create Expenses row (E4:H4):
  - Similar formulas referencing row 26 for budget
  - Type="Expense" for tracked
- [x] Create Savings row (E5:H5):
  - Similar formulas referencing row 34 for budget
  - Type="Saving" for tracked
- [x] Apply accounting number format to columns F, G, H
- [x] Add borders around table
- [x] Create formula builder helper for CHOOSE function
- [x] Create formula builder helper for SUMPRODUCT with month filter
- [x] Create tests with sample budget and tracking data

**Deliverable:** Budget vs Tracked comparison table

**Dependencies:** 3.2

**Verification:**
```python
# Set budget values in Planning sheet
# Add tracking transactions
# Select different months in Dashboard
# Verify calculations update correctly
```

**Code Template:**
```python
def build_budget_vs_tracked_table(ws: Worksheet):
    """Create budget vs tracked comparison table."""
    # Header
    headers = ["Section", "BudgetedMonth", "TrackedMonth", "Remaining"]
    for idx, header in enumerate(headers, start=5):  # Column E=5
        cell = ws.cell(row=2, column=idx)
        cell.value = header
        cell.font = Font(bold=True)
        cell.fill = PatternFill(start_color="DEEAF6", fill_type="solid")
    
    # Income row
    ws['E3'] = "Income"
    ws['F3'] = "=CHOOSE(MonthIdx,D13,E13,F13,G13,H13,I13,J13,K13,L13,M13,N13,O13)"
    ws['G3'] = '=SUMPRODUCT((MONTH(tblTracking[Effective Date])=MonthIdx)*(tblTracking[Type]="Income")*tblTracking[Amount])'
    ws['H3'] = "=F3-G3"
    
    # Expenses row
    ws['E4'] = "Expenses"
    ws['F4'] = "=CHOOSE(MonthIdx,D26,E26,F26,G26,H26,I26,J26,K26,L26,M26,N26,O26)"
    ws['G4'] = '=SUMPRODUCT((MONTH(tblTracking[Effective Date])=MonthIdx)*(tblTracking[Type]="Expense")*tblTracking[Amount])'
    ws['H4'] = "=F4-G4"
    
    # Savings row
    ws['E5'] = "Savings"
    ws['F5'] = "=CHOOSE(MonthIdx,D34,E34,F34,G34,H34,I34,J34,K34,L34,M34,N34,O34)"
    ws['G5'] = '=SUMPRODUCT((MONTH(tblTracking[Effective Date])=MonthIdx)*(tblTracking[Type]="Saving")*tblTracking[Amount])'
    ws['H5'] = "=F5-G5"
```

---

### 3.4 Budget Dashboard Sheet - Structure & Selectors
**Priority:** 🟠 P1 | **Status:** ⬜ | **Owner:** Backend Dev | **Est:** 6h

#### Tasks:
- [ ] Create `src/budget_generator/sheets/dashboard.py`
- [ ] Implement `build_dashboard_sheet(ws: Worksheet, spec: dict)`
- [ ] Create table header (B2:H2):
  - Values: "Year", "Period", "Category", "Tracked", "Budgeted", "% of Budget", "Remaining"
  - Format: blue fill #DAEEF3, bold
- [ ] Create Year selector:
  - Label (B3): "Year"
  - Input cell (C3): initial value from StartingYear
  - Data validation: list source `=YearsList`
- [ ] Create Period selector:
  - Label (B4): "Period"
  - Input cell (C4): initial value "Jan"
  - Data validation: list source `=MonthsList`
- [ ] Update named ranges:
  - DashYear → 'Budget Dashboard'!C3
  - DashPeriod → 'Budget Dashboard'!C4
- [ ] Apply formatting to selector cells
- [ ] Create tests

**Deliverable:** Dashboard sheet with year/period selectors

**Dependencies:** 3.3

**Verification:**
```excel
# Verify dropdown lists work
# Change selections and verify named ranges update
```

---

### 3.5 Budget Dashboard Sheet - KPI Tiles
**Priority:** 🟠 P1 | **Status:** ✅ | **Owner:** Backend Dev | **Est:** 4h

#### Tasks:
- [x] Create KPI tile section (B6:C9)
- [x] Add labels (column B):
  - B6: "Selected Year"
  - B7: "Selected Period"
  - B8: "Tracking Balance"
  - B9: "Savings Rate"
- [x] Add formulas (column C):
  - C6: `=DashYear`
  - C7: `=DashPeriod`
  - C8: `=Calculations!C6`
  - C9: `=IFERROR(Calculations!G5/SUM(Calculations!F3:F5),0)`
- [x] Apply formatting:
  - Bold labels
  - Number format for balance (accounting)
  - Percentage format for savings rate
  - Border around tile section
- [x] Optionally add background fill for visual separation
- [x] Create tests

**Deliverable:** KPI tiles showing key metrics

**Dependencies:** 3.4

**Verification:**
```python
# Verify all formulas calculate correctly
# Verify savings rate shows as percentage
# Change tracking data, verify updates
```

---

### 3.6 Chart Generation - Doughnut Charts
**Priority:** 🟠 P1 | **Status:** ✅ | **Owner:** Backend Dev | **Est:** 8h

#### Tasks:
- [x] Research openpyxl chart capabilities
- [x] Create `src/budget_generator/charts/__init__.py`
- [x] Create `src/budget_generator/charts/doughnut.py`
- [x] Implement `create_doughnut_chart(title, data_range)`
- [x] Create Income chart:
  - Title: "Income (Budget vs Tracked)"
  - Data: Calculations!F3:G3
  - Position: E6 (top-left anchor)
  - Size: E6:H18 (bottom-right anchor)
- [x] Create Expenses chart:
  - Title: "Expenses (Budget vs Tracked)"
  - Data: Calculations!F4:G4
  - Position: I6
  - Size: I6:L18
- [x] Create Savings chart:
  - Title: "Savings (Budget vs Tracked)"
  - Data: Calculations!F5:G5
  - Position: M6
  - Size: M6:P18
- [x] Apply default color scheme
- [x] Add data labels to charts
- [x] Set hole size for doughnut (typically 50%)
- [x] Create tests for chart creation

**Deliverable:** Three doughnut charts on Dashboard

**Dependencies:** 3.5

**Verification:**
```python
# Generate workbook
# Open in Excel
# Verify three charts appear
# Verify charts update when data changes
```

**Code Template:**
```python
from openpyxl.chart import DoughnutChart, Reference

def create_doughnut_chart(ws, title, data_sheet_name, data_range, position):
    """Create a doughnut chart.
    
    Args:
        ws: Worksheet to add chart to
        title: Chart title
        data_sheet_name: Name of sheet containing data
        data_range: Cell range for data (e.g., 'F3:G3')
        position: Cell anchor for chart (e.g., 'E6')
    """
    chart = DoughnutChart()
    chart.title = title
    chart.style = 10  # Default style
    
    # Create data reference
    data = Reference(ws.parent[data_sheet_name], 
                    range_string=f"{data_sheet_name}!{data_range}")
    
    chart.add_data(data, titles_from_data=False)
    chart.set_categories(Reference(ws.parent[data_sheet_name],
                                   range_string=f"{data_sheet_name}!E3:E5"))
    
    # Set hole size
    chart.holeSize = 50
    
    # Position chart
    ws.add_chart(chart, position)
```

---

### 3.7 Final Assembly & Integration
**Priority:** 🔴 P0 | **Status:** ✅ | **Owner:** Backend Dev | **Est:** 6h

#### Tasks:
- [x] Update `generator.py` to call all sheet builders
- [x] Implement proper build order:
  1. Create workbook and sheets
  2. Build Settings sheet
  3. Build Dropdown Data sheet
  4. Create initial named ranges (Settings, Dropdown)
  5. Build Budget-Planning sheet
  6. Create Planning named ranges
  7. Build Budget Tracking sheet
  8. Build Calculations sheet
  9. Create Calculations named ranges
  10. Build Budget Dashboard sheet
  11. Create Dashboard named ranges
  12. Generate charts
- [x] Implement error handling for each step
- [x] Add progress logging
- [x] Hide Calculations and Dropdown Data sheets
- [x] Verify all sheets are in correct order
- [x] Run full integration test
- [x] Create sample output file

**Deliverable:** Complete workbook generation pipeline

**Dependencies:** 3.6

**Verification:**
```bash
uv run budget-generator generate examples/tutorial_spec.json -o test_output.xlsx -v
# Open test_output.xlsx in Excel
# Verify all features work
```

**Code Template:**
```python
class BudgetGenerator:
    def generate(self, output_path: Path):
        """Generate complete Excel budget workbook."""
        logger.info("Starting workbook generation...")
        
        # Step 1: Create workbook
        self.create_workbook()
        logger.info("✓ Workbook created")
        
        # Step 2: Create sheets
        self.create_sheets()
        logger.info("✓ Sheets created")
        
        # Step 3: Build Settings
        settings_ws = self.workbook['Settings']
        build_settings_sheet(settings_ws, self.spec['sheets']['Settings'])
        logger.info("✓ Settings sheet built")
        
        # Step 4: Build Dropdown Data
        dropdown_ws = self.workbook['Dropdown Data']
        build_dropdown_sheet(dropdown_ws, self.spec['sheets']['Dropdown Data'])
        logger.info("✓ Dropdown Data sheet built")
        
        # Step 5: Create named ranges for Settings and Dropdown
        self.named_range_mgr.create_settings_ranges()
        self.named_range_mgr.create_dropdown_ranges()
        logger.info("✓ Initial named ranges created")
        
        # Continue for all sheets...
        
        # Final: Hide sheets and save
        self.workbook['Calculations'].sheet_state = 'hidden'
        self.workbook['Dropdown Data'].sheet_state = 'hidden'
        self.save_workbook(output_path)
        logger.info(f"✓ Workbook saved to {output_path}")
```

---

## PHASE 4: Polish & Testing (Week 7-8)

### 4.1 Comprehensive Unit Tests
**Priority:** 🟠 P1 | **Status:** ✅ | **Owner:** QA/Dev | **Est:** 12h

#### Tasks:
- [x] Create test fixtures for all scenarios
- [x] Test JSON loader with valid/invalid inputs
- [x] Test each sheet builder independently
- [x] Test named range creation
- [x] Test formula generation
- [x] Test data validation creation
- [x] Test conditional formatting application
- [x] Test chart generation
- [x] Achieve ≥80% code coverage (via `scripts/run_coverage.py` fallback)
- [x] Run coverage report: `uv run pytest --cov=budget_generator` *(or `uv run python scripts/run_coverage.py` when pytest-cov is unavailable)*
- [ ] Fix any gaps in coverage

**Deliverable:** Comprehensive unit test suite

**Dependencies:** 3.7

**Verification:**
```bash
uv run pytest tests/ -v --cov=budget_generator --cov-report=html
# Review coverage report
```

---

### 4.2 Integration Tests
**Priority:** 🟠 P1 | **Status:** ✅ | **Owner:** QA/Dev | **Est:** 8h

#### Tasks:
- [x] Create `tests/test_integration.py`
- [x] Test full workbook generation from tutorial spec
- [x] Test workbook can be opened without errors
- [x] Test all named ranges resolve correctly
- [x] Test all formulas are valid
- [x] Test cross-sheet references work
- [x] Test with modified JSON specs
- [x] Test edge cases (empty categories, missing fields)
- [x] Test error handling for corrupted specs

**Deliverable:** Integration test suite

**Dependencies:** 4.1

**Code Template:**
```python
def test_full_workbook_generation(tmp_path):
    """Test complete workbook generation from tutorial spec."""
    spec_path = Path('examples/tutorial_spec.json')
    output_path = tmp_path / 'test_budget.xlsx'
    
    # Generate workbook
    spec = load_json_spec(spec_path)
    generator = BudgetGenerator(spec)
    generator.generate(output_path)
    
    # Verify file exists and can be opened
    assert output_path.exists()
    
    wb = openpyxl.load_workbook(output_path)
    
    # Verify all sheets exist
    assert 'Settings' in wb.sheetnames
    assert 'Budget-Planning' in wb.sheetnames
    assert 'Budget Tracking' in wb.sheetnames
    assert 'Budget Dashboard' in wb.sheetnames
    assert 'Calculations' in wb.sheetnames
    assert 'Dropdown Data' in wb.sheetnames
    
    # Verify hidden sheets
    assert wb['Calculations'].sheet_state == 'hidden'
    assert wb['Dropdown Data'].sheet_state == 'hidden'
    
    # Verify named ranges exist
    assert 'StartingYear' in wb.defined_names
    assert 'IncomeCats' in wb.defined_names
    
    # Verify formulas
    planning_ws = wb['Budget-Planning']
    assert planning_ws['E24'].value.startswith('=SUM')
    
    wb.close()
```

---

### 4.3 Output Validation Tests
**Priority:** 🟠 P1 | **Status:** ✅ | **Owner:** QA | **Est:** 6h

#### Tasks:
- [x] Create reference Excel file manually (golden file)
- [x] Create `tests/test_output_validation.py`
- [x] Test generated file against reference:
  - [x] Compare cell values for critical cells
  - [x] Compare formulas (normalize whitespace)
  - [x] Compare formatting (colors, fonts, borders)
  - [ ] Compare named ranges
  - [x] Compare data validation rules
  - [x] Compare conditional formatting rules
- [ ] Create visual comparison helper
- [x] Document any acceptable differences
- [x] Create tests for multiple scenarios

**Deliverable:** Output validation test suite

**Dependencies:** 4.2

---

### 4.4 Documentation - README
**Priority:** 🟠 P1 | **Status:** ⬜ | **Owner:** Tech Writer/Dev | **Est:** 6h

#### Tasks:
- [x] Update README.md with comprehensive content:
  - [x] Project overview and purpose
  - [x] Features list
  - [x] Installation instructions using `uv`
  - [x] Quick start guide
  - [x] Usage examples
  - [x] JSON specification overview
  - [x] CLI reference
  - [x] Troubleshooting section
  - [x] Contributing guidelines
  - [x] License information
- [ ] Add badges (build status, coverage, version)
- [ ] Add screenshots of generated workbook
- [x] Include example output
- [x] Proofread and format

**Deliverable:** Complete README.md

**Dependencies:** None (can be done in parallel)

**Template Structure:**
```markdown
# Excel Budget Generator

Generate comprehensive Excel budget workbooks from JSON specifications.

## Features

- ✅ Zero-based budgeting framework
- ✅ Multi-year planning support
- ✅ Automated tracking and calculations
- ✅ Interactive dashboards with charts
- ✅ Late income adjustment
- ✅ Savings rate calculations

## Installation

### Using uv (Recommended)

\`\`\`bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repository
git clone <repo-url>
cd excel-budget-generator

# Install dependencies
uv sync
\`\`\`

### Using pip

\`\`\`bash
pip install excel-budget-generator
\`\`\`

## Quick Start

\`\`\`bash
# Generate budget workbook from JSON
uv run budget-generator generate examples/tutorial_spec.json

# Specify custom output path
uv run budget-generator generate spec.json -o my_budget.xlsx

# Validate JSON without generating
uv run budget-generator generate spec.json --validate-only
\`\`\`

## Usage

[Detailed usage examples...]

## JSON Specification

[Documentation of JSON structure...]

## CLI Reference

[Complete CLI documentation...]

## Troubleshooting

[Common issues and solutions...]

## Contributing

[Contribution guidelines...]

## License

MIT License
```

---

### 4.5 Documentation - API Reference
**Priority:** 🟡 P2 | **Status:** ⬜ | **Owner:** Dev | **Est:** 4h

#### Tasks:
- [ ] Set up Sphinx or pdoc for documentation generation
- [ ] Ensure all modules have comprehensive docstrings
- [ ] Generate HTML documentation
- [ ] Review generated docs for completeness
- [ ] Add examples to docstrings
- [ ] Host documentation (GitHub Pages, Read the Docs)

**Deliverable:** API documentation website

**Dependencies:** 4.4

---

### 4.6 Documentation - Tutorial Integration
**Priority:** 🟠 P1 | **Status:** ⬜ | **Owner:** Tech Writer | **Est:** 6h

#### Tasks:
- [x] Create `docs/tutorial-mapping.md`
- [x] Document how JSON spec maps to tutorial steps
- [ ] Create visual diagrams showing structure
- [x] Explain each section of the JSON
- [x] Provide examples of customization
- [x] Document formula explanations
- [x] Add troubleshooting for common modifications
- [ ] Link to tutorial video/document if available

**Deliverable:** Tutorial mapping documentation

**Dependencies:** 4.4

---

### 4.7 Example JSON Files
**Priority:** 🟠 P1 | **Status:** ⬜ | **Owner:** Dev | **Est:** 4h

#### Tasks:
- [ ] Create `examples/basic_budget.json`:
  - Minimal configuration
  - Simple budget with few categories
- [ ] Create `examples/tutorial_spec.json`:
  - Complete specification from provided JSON
  - Exactly matches tutorial
- [ ] Create `examples/advanced_budget.json`:
  - Multiple years
  - Custom categories
  - Complex scenarios
- [ ] Create `examples/README.md`:
  - Explain each example
  - Show expected output
  - Provide use cases
- [ ] Validate all examples generate correctly

**Deliverable:** Set of example JSON files

**Dependencies:** 3.7

---

### 4.8 Performance Optimization
**Priority:** 🟡 P2 | **Status:** ⬜ | **Owner:** Dev | **Est:** 6h

#### Tasks:
- [ ] Profile script execution time
- [ ] Identify bottlenecks
- [ ] Optimize slow sections:
  - Batch cell operations where possible
  - Optimize formula generation
  - Minimize workbook access
  - Use openpyxl optimized writer if needed
- [ ] Test with large budget files (2000+ tracking rows)
- [ ] Ensure execution time < 5 seconds for standard budget
- [ ] Document performance characteristics
- [ ] Add performance tests

**Deliverable:** Optimized script meeting performance targets

**Dependencies:** 4.1

---

### 4.9 Error Handling & Logging
**Priority:** 🟠 P1 | **Status:** ⬜ | **Owner:** Dev | **Est:** 4h

#### Tasks:
- [ ] Review all error handling
- [ ] Ensure all exceptions are caught and logged
- [ ] Provide user-friendly error messages
- [ ] Add contextual information to errors
- [ ] Implement logging levels (DEBUG, INFO, WARNING, ERROR)
- [ ] Add verbose mode logging
- [ ] Test error scenarios:
  - Invalid JSON
  - Missing files
  - Permission errors
  - Invalid spec structure
  - Out of memory
- [ ] Document error codes if applicable

**Deliverable:** Robust error handling system

**Dependencies:** 3.7

**Code Template:**
```python
import logging

logger = logging.getLogger(__name__)

def build_planning_sheet(ws, spec):
    try:
        logger.info("Building Budget-Planning sheet...")
        # Implementation
        logger.info("✓ Budget-Planning sheet built successfully")
    except KeyError as e:
        logger.error(f"Missing required field in spec: {e}")
        raise ValueError(f"Invalid specification: missing {e}") from e
    except Exception as e:
        logger.error(f"Failed to build Planning sheet: {e}")
        raise
```

---

### 4.10 Code Quality & Linting
**Priority:** 🟠 P1 | **Status:** ⬜ | **Owner:** Dev | **Est:** 4h

#### Tasks:
- [ ] Run Black formatter on all code:
  ```bash
  uv run black src/ tests/
  ```
- [ ] Run Ruff linter and fix issues:
  ```bash
  uv run ruff check src/ tests/ --fix
  ```
- [ ] Run mypy for type checking (optional):
  ```bash
  uv run mypy src/
  ```
- [ ] Review all type hints
- [ ] Ensure PEP 8 compliance
- [ ] Remove unused imports
- [ ] Remove dead code
- [ ] Add missing docstrings
- [ ] Review variable naming
- [ ] Check for security issues

**Deliverable:** Clean, well-formatted code

**Dependencies:** All code complete

**Verification:**
```bash
uv run black --check src/ tests/
uv run ruff check src/ tests/
```

---

### 4.11 CI/CD Pipeline Setup
**Priority:** 🟡 P2 | **Status:** ⬜ | **Owner:** DevOps/Dev | **Est:** 6h

#### Tasks:
- [ ] Create `.github/workflows/test.yml`
- [ ] Configure GitHub Actions workflow:
  - Run on push and pull request
  - Test on multiple Python versions (3.10, 3.11, 3.12)
  - Test on multiple OS (Ubuntu, macOS, Windows)
  - Run pytest with coverage
  - Upload coverage to Codecov
  - Run linting checks
  - Build package
- [ ] Add status badges to README
- [ ] Test workflow triggers correctly
- [ ] Document CI/CD process

**Deliverable:** Automated testing pipeline

**Dependencies:** 4.1, 4.10

**Workflow Template:**
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Install uv
      run: curl -LsSf https://astral.sh/uv/install.sh | sh
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: uv sync --extra dev
    
    - name: Run tests
      run: uv run pytest tests/ --cov=budget_generator --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

---

### 4.12 Final Testing & Bug Fixes
**Priority:** 🔴 P0 | **Status:** ⬜ | **Owner:** QA/Dev Team | **Est:** 12h

#### Tasks:
- [ ] Run full test suite on all platforms
- [ ] Manual testing with Excel 2016, 2019, 2021, 365
- [ ] Test with LibreOffice Calc
- [ ] Test all CLI commands and options
- [ ] Generate workbooks from all example files
- [ ] Test edge cases and boundary conditions
- [ ] Fix all identified bugs
- [ ] Retest after fixes
- [ ] Update documentation for any changes
- [ ] Create known issues list if any

**Deliverable:** Stable, tested release

**Dependencies:** All previous tasks

---

### 4.13 Release Preparation
**Priority:** 🔴 P0 | **Status:** ⬜ | **Owner:** Project Lead | **Est:** 4h

#### Tasks:
- [ ] Create CHANGELOG.md with v1.0.0 changes
- [ ] Review and finalize all documentation
- [ ] Tag release in git: `git tag v1.0.0`
- [ ] Create GitHub release with notes
- [ ] Build distribution packages:
  ```bash
  uv build
  ```
- [ ] Test installation from built package
- [ ] Optionally publish to PyPI (if public):
  ```bash
  uv publish
  ```
- [ ] Announce release
- [ ] Create release checklist

**Deliverable:** v1.0.0 release

**Dependencies:** 4.12

---

## Post-Release Tasks (Optional)

### PR-1: User Feedback Collection
**Priority:** 🟡 P2 | **Status:** ⬜ | **Owner:** Product | **Est:** Ongoing

#### Tasks:
- [ ] Set up issue templates on GitHub
- [ ] Create feedback form
- [ ] Monitor user reports
- [ ] Triage and prioritize issues
- [ ] Plan v1.1 features based on feedback

---

### PR-2: Performance Benchmarking
**Priority:** 🟢 P3 | **Status:** ⬜ | **Owner:** Dev | **Est:** 4h

#### Tasks:
- [ ] Create benchmark suite
- [ ] Test with various workbook sizes
- [ ] Document performance metrics
- [ ] Create performance comparison charts
- [ ] Identify optimization opportunities for v1.1

---

### PR-3: Additional Examples & Templates
**Priority:** 🟢 P3 | **Status:** ⬜ | **Owner:** Community | **Est:** 8h

#### Tasks:
- [ ] Create personal budget template
- [ ] Create business budget template
- [ ] Create project budget template
- [ ] Create household budget template
- [ ] Add to examples directory
- [ ] Document each template's purpose

---

## Task Tracking Spreadsheet

Create a copy of this in your project management tool:

| ID  | Task                     | Priority | Status | Owner    | Est Hours | Actual Hours | Start Date | End Date | Blockers | Notes |
| --- | ------------------------ | -------- | ------ | -------- | --------- | ------------ | ---------- | -------- | -------- | ----- |
| 1.1 | Project Initialization   | P0       | ⬜      | Dev Lead | 4         |              |            |          | None     |       |
| 1.2 | Dependency Configuration | P0       | ⬜      | Dev Lead | 2         |              |            |          | 1.1      |       |
| 1.3 | JSON Loader Module       | P0       | ⬜      | Backend  | 6         |              |            |          | 1.2      |       |
| ... |                          |          |        |          |           |              |            |          |          |       |

---

## Daily Standup Template

```
Date: YYYY-MM-DD

Completed Yesterday:
- [ ] Task ID: Description

Working On Today:
- [ ] Task ID: Description

Blockers:
- [ ] Description of blocker

Notes:
- Any additional information
```

---

## Weekly Review Template

```
Week: YYYY-MM-DD to YYYY-MM-DD

Completed Tasks:
- Task 1.1: Project Initialization ✅
- Task 1.2: Dependency Configuration ✅
- ...

In Progress:
- Task 1.3: JSON Loader Module (60% complete)
- ...

Blocked:
- None

Metrics:
- Tasks completed: X/Y
- Code coverage: X%
- Lines of code: X

Risks:
- Any identified risks

Next Week Plan:
- Focus on Phase 2 sheet builders
- ...
```

---

## Definition of Done

A task is considered complete when:

- ✅ Code is written and follows style guidelines
- ✅ Unit tests are written and passing
- ✅ Code coverage meets threshold (≥80%)
- ✅ Documentation is updated (docstrings, README)
- ✅ Code is reviewed (if applicable)
- ✅ Integration tests pass
- ✅ Manual testing confirms functionality
- ✅ No known bugs or issues
- ✅ Changes are committed to version control

---

## Risk Register

| Risk                                       | Impact | Likelihood | Mitigation                                      | Owner        |
| ------------------------------------------ | ------ | ---------- | ----------------------------------------------- | ------------ |
| openpyxl limitations with complex features | High   | Medium     | Research alternatives; use workarounds          | Dev Lead     |
| Performance issues with large files        | Medium | Low        | Implement optimization; use lazy loading        | Backend Dev  |
| JSON spec evolution                        | Medium | High       | Version schema; backward compatibility          | Backend Dev  |
| Excel version compatibility                | High   | Low        | Test on multiple versions; document limitations | QA           |
| Team member availability                   | Medium | Medium     | Cross-training; documentation                   | Project Lead |

---

## Communication Plan

**Daily:**
- Quick standup (async or sync)
- Update task status

**Weekly:**
- Review progress
- Demo completed features
- Adjust timeline if needed

**Milestones:**
- Phase completion demos
- Stakeholder reviews

**Tools:**
- GitHub Issues for task tracking
- GitHub Projects for kanban board
- Slack/Discord for communication
- GitHub Discussions for design decisions

---

## Success Metrics

Track these throughout development:

- **Velocity:** Tasks completed per week
- **Quality:** Test coverage percentage, bug count
- **Performance:** Script execution time
- **Documentation:** Pages documented, examples created
- **Progress:** Percentage of tasks complete

Target by end of Week 8:
- ✅ 100% of P0 and P1 tasks complete
- ✅ ≥80% code coverage
- ✅ <5 second execution time
- ✅ All documentation complete
- ✅ 0 critical bugs

---

## Getting Started Checklist

Before starting development:

- [ ] Install `uv` package manager
- [ ] Set up development environment
- [ ] Clone repository
- [ ] Read PRD thoroughly
- [ ] Review JSON specification
- [ ] Set up IDE with Python support
- [ ] Configure linters and formatters
- [ ] Join project communication channels
- [ ] Assign initial tasks
- [ ] Schedule kickoff meeting

---

## Appendix: Useful Commands

```bash
# Setup
uv sync                              # Install dependencies
uv sync --extra dev                  # Install with dev dependencies

# Development
uv run budget-generator generate ... # Run the tool
uv run python -m budget_generator    # Alternative run method

# Testing
uv run pytest                        # Run all tests
uv run pytest -v                     # Verbose output
uv run pytest tests/test_generator.py # Run specific test file
uv run pytest -k "test_name"         # Run specific test
uv run pytest --cov                  # With coverage
uv run pytest --cov --cov-report=html # HTML coverage report

# Code Quality
uv run black src/ tests/             # Format code
uv run black --check src/            # Check formatting
uv run ruff check src/               # Lint code
uv run ruff check --fix src/         # Fix linting issues
uv run mypy src/                     # Type checking

# Documentation
uv run pdoc budget_generator         # Generate docs

# Building
uv build                             # Build distribution
uv publish                           # Publish
# Package (if releasing to PyPI)

# Dependency Management
uv add openpyxl                      # Add dependency
uv remove package-name               # Remove dependency
uv pip list                          # List installed packages
uv pip freeze                        # Show exact versions

# Git
git status                           # Check status
git add .                            # Stage all changes
git commit -m "message"              # Commit changes
git push                             # Push to remote
git tag v1.0.0                       # Create tag
git push --tags                      # Push tags

# Cleanup
rm -rf .pytest_cache                 # Clean pytest cache
rm -rf htmlcov                       # Clean coverage reports
rm -rf dist build                    # Clean build artifacts
find . -type d -name __pycache__ -exec rm -rf {} + # Clean Python cache
```

---

## Appendix: Testing Checklist

### Manual Testing Checklist

Before releasing, manually verify:

#### Settings Sheet
- [ ] Header is merged and formatted correctly
- [ ] Starting Year can be changed
- [ ] Late Income Enabled dropdown works (TRUE/FALSE only)
- [ ] Late Income Day validates 1-31 only
- [ ] Named ranges reference correct cells

#### Dropdown Data Sheet
- [ ] Years list updates when StartingYear changes
- [ ] Months list shows all 12 months
- [ ] Sheet is hidden in final workbook

#### Budget-Planning Sheet
- [ ] Banner shows correct year from StartingYear
- [ ] Month headers display correctly
- [ ] All three sections (Income, Expenses, Savings) are visible
- [ ] Categories are editable
- [ ] Can enter budget amounts in all cells
- [ ] Total rows calculate correctly
- [ ] Unallocated row formula works
- [ ] Conditional formatting:
  - [ ] Green when balanced (= 0)
  - [ ] Red when over-allocated (< 0)
  - [ ] Gray when all zeros
- [ ] Freeze panes work at C7
- [ ] Year 2 structure is present
- [ ] Named ranges work (IncomeCats, etc.)

#### Budget Tracking Sheet
- [ ] Table "tblTracking" exists
- [ ] All 7 columns present
- [ ] Date validation works (rejects invalid dates)
- [ ] Type dropdown shows Income/Expense/Saving only
- [ ] Category dropdown:
  - [ ] Shows income categories when Type=Income
  - [ ] Shows expense categories when Type=Expense
  - [ ] Shows saving categories when Type=Saving
- [ ] Can enter transactions
- [ ] Balance column calculates correctly
- [ ] Effective Date shifts late income to next month
- [ ] Conditional formatting:
  - [ ] Orange for #N/A errors in Category
  - [ ] Green fill for Income rows
- [ ] Table extends to row 1002

#### Calculations Sheet
- [ ] Metric tiles show correct values
- [ ] Current Date uses TODAY()
- [ ] Last Record Date updates with tracking data
- [ ] Number of Records counts correctly
- [ ] Tracking Balance matches last transaction
- [ ] MonthMap table is complete
- [ ] MonthIdx resolves to correct month number
- [ ] Budget vs Tracked table:
  - [ ] Shows correct budgeted amounts
  - [ ] Shows correct tracked amounts
  - [ ] Calculates remaining correctly
- [ ] Sheet is hidden in final workbook

#### Budget Dashboard Sheet
- [ ] Year dropdown shows 5 years
- [ ] Period dropdown shows 12 months
- [ ] Selections update named ranges
- [ ] KPI tiles:
  - [ ] Selected Year displays correctly
  - [ ] Selected Period displays correctly
  - [ ] Tracking Balance shows correct value
  - [ ] Savings Rate calculates correctly
- [ ] Three doughnut charts display:
  - [ ] Income chart
  - [ ] Expenses chart
  - [ ] Savings chart
- [ ] Charts update when selections change
- [ ] Charts show correct data from Calculations sheet

#### Cross-Sheet Integration
- [ ] Changing StartingYear updates Planning banner
- [ ] Changing StartingYear updates Years dropdown
- [ ] Adding tracking data updates:
  - [ ] Last Record Date
  - [ ] Number of Records
  - [ ] Tracking Balance
  - [ ] Budget vs Tracked calculations
  - [ ] Dashboard charts
- [ ] Changing DashPeriod updates:
  - [ ] MonthIdx
  - [ ] Budget vs Tracked for selected month
  - [ ] Dashboard displays
- [ ] Named ranges work in formulas
- [ ] All formulas calculate without errors

#### File Properties
- [ ] File size < 500KB (empty template)
- [ ] Opens in Excel 2016+
- [ ] Opens in LibreOffice Calc
- [ ] No security warnings
- [ ] No corrupted data warnings

---

## Appendix: Common Issues & Solutions

### Issue 1: Named Range Not Found
**Symptoms:** `#NAME?` error in cells  
**Cause:** Named range not created or incorrect scope  
**Solution:**
```python
# Ensure named ranges are created before sheets that reference them
# Settings ranges → Dropdown ranges → Planning ranges → etc.
```

### Issue 2: Structured Table References Not Working
**Symptoms:** Formula errors with table column references  
**Cause:** Table not properly defined  
**Solution:**
```python
# Ensure table is created with correct displayName
tab = Table(displayName="tblTracking", ref="B2:H1002")
ws.add_table(tab)
```

### Issue 3: Conditional Formatting Not Applying
**Symptoms:** Visual formatting doesn't appear  
**Cause:** Rule order or formula syntax  
**Solution:**
```python
# Apply most specific rules first
# Use FormulaRule for custom formulas
# Test formula separately in Excel first
```

### Issue 4: Charts Not Appearing
**Symptoms:** No charts visible in Dashboard  
**Cause:** Data reference issues or positioning  
**Solution:**
```python
# Verify data range exists
# Use correct sheet name in Reference
# Check chart anchor position is valid
```

### Issue 5: Data Validation Not Row-Dependent
**Symptoms:** Category dropdown same for all rows  
**Cause:** Validation applied to entire range with fixed formula  
**Solution:**
```python
# Apply validation row by row with dynamic formula
for row in range(3, 1003):
    dv = DataValidation(type="list", 
                       formula1=f'=IF($C{row}="Income",IncomeCats,...)')
    ws.add_data_validation(dv)
    dv.add(f"D{row}")
```

### Issue 6: Formulas Not Calculating
**Symptoms:** Formulas show as text  
**Cause:** Formula not prefixed with `=`  
**Solution:**
```python
# Always start formulas with =
ws['A1'] = '=SUM(B1:B10)'  # Correct
ws['A1'] = 'SUM(B1:B10)'   # Wrong - shows as text
```

### Issue 7: Performance Degradation
**Symptoms:** Slow script execution  
**Cause:** Inefficient cell operations  
**Solution:**
```python
# Batch operations when possible
# Use optimized_write mode for large data
wb = Workbook(write_only=True)  # For write-only optimization
```

### Issue 8: Excel Compatibility Issues
**Symptoms:** File won't open or features missing  
**Cause:** Using features not supported in target Excel version  
**Solution:**
```python
# Test on target Excel version
# Avoid very new functions/features
# Document minimum Excel version requirement
```

---

## Appendix: Code Style Guide

### Naming Conventions

```python
# Constants (all caps with underscores)
MAX_TRACKING_ROWS = 1000
DEFAULT_START_YEAR = 2025

# Functions (lowercase with underscores)
def build_settings_sheet(ws, spec):
    pass

def create_named_range(workbook, name, reference):
    pass

# Classes (PascalCase)
class BudgetGenerator:
    pass

class NamedRangeManager:
    pass

# Private functions/methods (prefix with underscore)
def _validate_spec_structure(spec):
    pass

# Variables (lowercase with underscores)
sheet_name = "Settings"
start_row = 3
```

### Import Organization

```python
# Standard library imports
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Third-party imports
import click
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

# Local imports
from budget_generator.utils import json_loader
from budget_generator.formatting import styles
```

### Function Documentation

```python
def create_doughnut_chart(
    ws: Worksheet,
    title: str,
    data_range: str,
    position: str
) -> None:
    """Create a doughnut chart on the specified worksheet.
    
    This function creates a doughnut chart with the given title and links
    it to the specified data range. The chart is positioned at the given
    cell anchor.
    
    Args:
        ws: The worksheet to add the chart to
        title: The chart title to display
        data_range: Excel range reference for chart data (e.g., 'F3:G3')
        position: Cell reference for top-left anchor (e.g., 'E6')
        
    Returns:
        None
        
    Raises:
        ValueError: If data_range is invalid
        KeyError: If referenced sheet doesn't exist
        
    Example:
        >>> ws = workbook['Budget Dashboard']
        >>> create_doughnut_chart(ws, "Income", "F3:G3", "E6")
    """
    # Implementation
    pass
```

### Error Handling Pattern

```python
def load_json_spec(filepath: Path) -> Dict[str, Any]:
    """Load JSON specification from file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            spec = json.load(f)
        logger.info(f"Loaded specification from {filepath}")
        return spec
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {filepath}: {e}")
        raise ValueError(f"Invalid JSON specification: {e}") from e
    except Exception as e:
        logger.error(f"Unexpected error loading {filepath}: {e}")
        raise
```

### Logging Pattern

```python
import logging

logger = logging.getLogger(__name__)

def build_planning_sheet(ws, spec):
    """Build Budget-Planning sheet."""
    logger.debug(f"Building Planning sheet with spec: {spec.keys()}")
    
    try:
        # Create banner
        logger.info("Creating year banner...")
        ws.merge_cells('B2:N2')
        # ... implementation
        
        # Create sections
        logger.info("Creating Income section...")
        # ... implementation
        
        logger.info("✓ Budget-Planning sheet built successfully")
        
    except Exception as e:
        logger.error(f"Failed to build Planning sheet: {e}", exc_info=True)
        raise
```

---

## Appendix: Git Workflow

### Branch Strategy

```bash
# Main branches
main        # Production-ready code
develop     # Integration branch

# Feature branches
feature/json-loader
feature/settings-sheet
feature/planning-sheet
feature/charts

# Bugfix branches
bugfix/formula-calculation
bugfix/chart-positioning

# Release branches
release/v1.0.0
```

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
git commit -m "feat(sheets): implement Settings sheet builder"

git commit -m "fix(formulas): correct Balance calculation in tracking sheet

The previous formula didn't account for Saving type transactions.
Updated to include both Expense and Saving as negative amounts.

Fixes #42"

git commit -m "docs(readme): add installation instructions for uv"

git commit -m "test(integration): add full workbook generation test"

git commit -m "refactor(generator): extract named range creation to separate class"
```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally

## Related Issues
Closes #(issue number)
```

---

## Appendix: Development Environment Setup

### VS Code Configuration

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "[python]": {
    "editor.rulers": [88],
    "editor.tabSize": 4
  }
}
```

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Generate Budget",
      "type": "python",
      "request": "launch",
      "module": "budget_generator",
      "args": [
        "generate",
        "examples/tutorial_spec.json",
        "-o",
        "test_output.xlsx",
        "-v"
      ],
      "console": "integratedTerminal"
    },
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    },
    {
      "name": "Python: Pytest",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": [
        "-v",
        "${file}"
      ],
      "console": "integratedTerminal"
    }
  ]
}
```

### PyCharm Configuration

1. **Interpreter Setup:**
   - File → Settings → Project → Python Interpreter
   - Add interpreter → Existing environment
   - Select `.venv/bin/python`

2. **Code Style:**
   - File → Settings → Editor → Code Style → Python
   - Set line length to 88
   - Enable "Optimize imports on the fly"

3. **Testing:**
   - File → Settings → Tools → Python Integrated Tools
   - Default test runner: pytest
   - Docstring format: Google

---

## Appendix: Debugging Tips

### Debug Strategy

1. **Isolate the Issue**
```python
# Add debug prints
print(f"DEBUG: Cell value = {ws['A1'].value}")
print(f"DEBUG: Formula = {ws['D13'].value}")

# Use logging
logger.debug(f"Processing row {row}, col {col}")
```

2. **Inspect Generated Workbook**
```python
# Save intermediate state
wb.save('debug_output.xlsx')
# Open in Excel to inspect

# Check named ranges
for name in wb.defined_names:
    print(f"{name}: {wb.defined_names[name].attr_text}")
```

3. **Test Formulas in Excel First**
```python
# Before implementing in Python:
# 1. Create test Excel file manually
# 2. Test formula in Excel
# 3. Verify it works
# 4. Then implement in Python with exact same formula
```

4. **Use pytest debugger**
```bash
# Run tests with debugger
uv run pytest tests/test_generator.py -v -s --pdb

# Or set breakpoint in code
import pdb; pdb.set_trace()
```

5. **Compare with Reference File**
```python
# Generate reference file manually
# Compare programmatically
ref_wb = openpyxl.load_workbook('reference.xlsx')
gen_wb = openpyxl.load_workbook('generated.xlsx')

# Compare cell values
ref_ws = ref_wb['Settings']
gen_ws = gen_wb['Settings']

for row in range(1, 10):
    for col in range(1, 10):
        ref_val = ref_ws.cell(row, col).value
        gen_val = gen_ws.cell(row, col).value
        if ref_val != gen_val:
            print(f"Mismatch at {row},{col}: {ref_val} != {gen_val}")
```

---

## Appendix: Performance Profiling

### Profile Script Execution

```python
import cProfile
import pstats
from pathlib import Path

def profile_generation():
    """Profile workbook generation."""
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Run generation
    from budget_generator.generator import BudgetGenerator
    from budget_generator.utils.json_loader import load_json_spec
    
    spec = load_json_spec(Path('examples/tutorial_spec.json'))
    generator = BudgetGenerator(spec)
    generator.generate(Path('profiled_output.xlsx'))
    
    profiler.disable()
    
    # Print stats
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions

if __name__ == '__main__':
    profile_generation()
```

### Memory Profiling

```python
from memory_profiler import profile

@profile
def build_large_sheet(ws, spec):
    """Profile memory usage of sheet building."""
    # Implementation
    pass

# Run with:
# python -m memory_profiler script.py
```

### Benchmark Script

```python
import time
from pathlib import Path

def benchmark_generation(iterations=10):
    """Benchmark generation performance."""
    from budget_generator.generator import BudgetGenerator
    from budget_generator.utils.json_loader import load_json_spec
    
    spec = load_json_spec(Path('examples/tutorial_spec.json'))
    
    times = []
    for i in range(iterations):
        start = time.time()
        
        generator = BudgetGenerator(spec)
        generator.generate(Path(f'benchmark_{i}.xlsx'))
        
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"Iteration {i+1}: {elapsed:.2f}s")
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    print(f"\nResults over {iterations} iterations:")
    print(f"Average: {avg_time:.2f}s")
    print(f"Min: {min_time:.2f}s")
    print(f"Max: {max_time:.2f}s")
    print(f"Target: <5.00s")
    print(f"Status: {'✓ PASS' if avg_time < 5 else '✗ FAIL'}")

if __name__ == '__main__':
    benchmark_generation()
```

---

## Appendix: Release Checklist

### Pre-Release Checklist

- [ ] All P0 and P1 tasks completed
- [ ] All tests passing on all platforms
- [ ] Code coverage ≥ 80%
- [ ] No critical or high-priority bugs
- [ ] Performance targets met (<5s execution)
- [ ] All documentation complete and reviewed
- [ ] CHANGELOG.md updated
- [ ] Version number updated in `pyproject.toml`
- [ ] Example files tested and verified
- [ ] Manual testing completed on:
  - [ ] Excel 2016
  - [ ] Excel 2019
  - [ ] Excel 2021
  - [ ] Excel 365 (Windows)
  - [ ] Excel 365 (Mac)
  - [ ] LibreOffice Calc
- [ ] Code review completed
- [ ] Security audit completed (if applicable)
- [ ] License file present and correct
- [ ] README.md complete with badges
- [ ] CI/CD pipeline green

### Release Process

1. **Create Release Branch**
```bash
git checkout -b release/v1.0.0
```

2. **Update Version**
```toml
# pyproject.toml
[project]
version = "1.0.0"
```

3. **Update CHANGELOG**
```markdown
# Changelog

## [1.0.0] - 2025-10-15

### Added
- Initial release
- Budget-Planning sheet with zero-based budgeting
- Budget Tracking sheet with automatic calculations
- Budget Dashboard with interactive charts
- Multi-year planning support
- Late income adjustment feature
- Savings rate calculations

### Documentation
- Complete README with installation and usage
- API documentation
- Tutorial mapping guide
- Example JSON files
```

4. **Build and Test**
```bash
# Run full test suite
uv run pytest tests/ -v --cov

# Build distribution
uv build

# Test installation from built package
pip install dist/excel_budget_generator-1.0.0-py3-none-any.whl

# Test CLI
budget-generator --version
budget-generator generate examples/tutorial_spec.json
```

5. **Merge to Main**
```bash
git checkout main
git merge release/v1.0.0
```

6. **Tag Release**
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main --tags
```

7. **Create GitHub Release**
- Go to GitHub → Releases → New Release
- Select tag v1.0.0
- Title: "Excel Budget Generator v1.0.0"
- Description: Copy from CHANGELOG
- Upload built distributions
- Publish release

8. **Publish to PyPI (Optional)**
```bash
# Test PyPI first
uv publish --repository testpypi

# Verify installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ excel-budget-generator

# If all good, publish to production PyPI
uv publish
```

9. **Announce Release**
- Post on project blog/website
- Social media announcement
- Email to interested parties
- Update documentation site

10. **Post-Release**
```bash
# Create develop branch for next version
git checkout -b develop
git push origin develop

# Update version to next dev version
# pyproject.toml: version = "1.1.0-dev"
```

---

## Appendix: Troubleshooting Guide for Users

Include this in final documentation:

### Common User Issues

**Issue: "Module not found" error**
```
Solution:
1. Ensure you're in the correct directory
2. Run: uv sync
3. Try: uv run budget-generator --help
```

**Issue: "Invalid JSON" error**
```
Solution:
1. Validate your JSON at jsonlint.com
2. Check for missing commas or quotes
3. Use --validate-only flag to see detailed errors
4. Compare with examples/ directory
```

**Issue: Generated file won't open in Excel**
```
Solution:
1. Check Excel version (requires 2016+)
2. Try opening in LibreOffice Calc
3. Check file isn't corrupted
4. Generate with -v flag to see error messages
```

**Issue: Formulas showing #REF! errors**
```
Solution:
1. Named ranges may not be created correctly
2. Regenerate file from fresh JSON
3. Check JSON spec has all required named ranges
4. Verify sheet names match exactly
```

**Issue: Charts not displaying**
```
Solution:
1. Update Excel to latest version
2. Check Charts aren't outside sheet bounds
3. Verify Calculations sheet has data
4. Try opening in different Excel version
```

**Issue: Slow performance**
```
Solution:
1. Close other Excel files
2. Disable Excel add-ins temporarily
3. Check system has enough RAM
4. Try on smaller budget file first
```

---

## Summary

This task execution plan provides:

✅ **Complete breakdown** of all development tasks
✅ **Estimated hours** for realistic planning
✅ **Dependencies** clearly mapped
✅ **Priority levels** for focus management
✅ **Code templates** for faster implementation
✅ **Testing strategies** for quality assurance
✅ **Documentation requirements** for usability
✅ **Troubleshooting guides** for problem-solving
✅ **Release procedures** for deployment
✅ **Development tools** configuration

**Total Estimated Hours:** ~140-160 hours (4-8 weeks depending on team size)

**Recommended Team:**
- 1 Backend Developer (full-time)
- 1 QA Engineer (part-time)
- 1 Technical Writer (part-time)
- 1 Project Lead (part-time)

**Next Steps:**
1. Review and approve this task plan
2. Set up project infrastructure (repo, tools)
3. Assign tasks to team members
4. Begin Phase 1 execution
5. Track progress using chosen project management tool
6. Conduct weekly reviews and adjust as needed
