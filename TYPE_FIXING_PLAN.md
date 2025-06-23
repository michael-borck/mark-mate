# Type Error Fixing Plan - MarkMate Codebase

## Summary
Total Errors: 484
Status: UNACCEPTABLE - Need systematic fixes

## Priority Categories

### PRIORITY 1: Critical Data Structure Issues (220+ errors)
**Root Cause**: Mixed data types in dictionary values - fields expected to be lists are sometimes int/str/bool

**Files Affected**:
- `analyzers/react_analysis.py` (200+ errors) - MOST CRITICAL
- `analyzers/web_validation.py` (50+ errors)  
- `analyzers/static_analysis.py` (20+ errors)

**Error Types**:
- `Cannot access attribute "append" for class "int/str/bool"`
- `Operator ">" not supported for types "int | str | list[Unknown]"`
- `Argument of type "X" cannot be assigned to parameter "obj" of type "Sized"`

### PRIORITY 2: Import Resolution Issues (50+ errors)
**Files Affected**:
- `extractors/web_extractor.py` (25+ errors)
- `extractors/react_extractor.py` (15+ errors)
- `extractors/office_extractor.py` (10+ errors)

**Error Types**:
- Missing or incorrect conditional imports
- Module not found errors
- Attribute access on potentially None types

### PRIORITY 3: Type Annotation Issues (50+ errors)
**Files Affected**:
- `core/llm_provider.py` (15+ errors)
- `cli/` modules (20+ errors)
- Various extractors (15+ errors)

**Error Types**:
- Missing return type annotations
- Incorrect parameter types
- Generic type specification errors

### PRIORITY 4: Optional/None Handling (50+ errors)
**Files Affected**:
- `extractors/github_extractor.py` (10+ errors)
- Various core modules (40+ errors)

**Error Types**:
- Optional member access without null checks
- None type assignments to non-optional fields

## Execution Plan

### Phase 1: Fix Critical Data Structure Issues (PRIORITY 1)
**Target**: Zero tolerance for mixed-type dictionary fields

1. **Fix `analyzers/react_analysis.py`** (200+ errors)
   - Rewrite data structure initialization with proper types
   - Fix all `append` calls on non-list types
   - Add proper type guards for dynamic data

2. **Fix `analyzers/web_validation.py`** (50+ errors)
   - Similar data structure fixes
   - Ensure consistent typing across methods

3. **Fix `analyzers/static_analysis.py`** (20+ errors)
   - Clean up remaining type issues

### Phase 2: Fix Import Resolution (PRIORITY 2)
**Target**: Clean conditional imports with proper type guards

1. **Fix `extractors/web_extractor.py`**
2. **Fix `extractors/react_extractor.py`**  
3. **Fix `extractors/office_extractor.py`**

### Phase 3: Fix Type Annotations (PRIORITY 3)
**Target**: Complete type annotations for all public interfaces

1. **Fix `core/llm_provider.py`**
2. **Fix CLI modules**
3. **Fix remaining extractors**

### Phase 4: Fix Optional/None Handling (PRIORITY 4)
**Target**: Proper null safety throughout

1. **Fix `extractors/github_extractor.py`**
2. **Fix remaining core modules**

## Success Criteria
- **0 errors** (not 496!)
- **< 50 warnings** (legitimate Any usage only)
- **All tests passing** (add tests as we fix)
- **No logic changes** (preserve functionality)

## Next Action
**Starting with**: `analyzers/react_analysis.py` - fixing the data structure initialization and type consistency issues that are causing 200+ errors.

This is the most critical file and will dramatically reduce our error count.