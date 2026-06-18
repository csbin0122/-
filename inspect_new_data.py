import os
import pandas as pd

def inspect_xlsx_sheets(filepath):
    try:
        xl = pd.ExcelFile(filepath)
        sheet_names = xl.sheet_names
        result = {}
        for name in sheet_names:
            df = xl.parse(name)
            
            # Stringify column names to prevent float attribute error
            df.columns = [str(c) for c in df.columns]
            
            # Check for SMILES-like columns
            smiles_cols = [c for c in df.columns if 'smiles' in c.lower()]
            
            # Check target candidates
            target_keywords = ['ld50', 'lc50', 'category', 'class', 'endpoint', 'reported_response', 'active', 'potency', 'value', 'activity', 'agonist', 'antagonist', 'hazard', 'call', 'result']
            target_cols = [c for c in df.columns if any(k in c.lower() for k in target_keywords)]
            
            unique_cas = df['CASRN'].nunique() if 'CASRN' in df.columns else 0
            unique_dtxsid = df['DTXSID'].nunique() if 'DTXSID' in df.columns else 0
            unique_name = df['Chemical_Name'].nunique() if 'Chemical_Name' in df.columns else 0
            
            mix_col = 'Mixture' if 'Mixture' in df.columns else None
            mix_counts = df[mix_col].value_counts().to_dict() if mix_col else {}
            
            result[name] = {
                "shape": df.shape,
                "columns": list(df.columns)[:15],
                "smiles_cols": smiles_cols,
                "target_cols": target_cols,
                "unique_cas": unique_cas,
                "unique_dtxsid": unique_dtxsid,
                "unique_name": unique_name,
                "mix_counts": mix_counts
            }
            if smiles_cols:
                for sc in smiles_cols:
                    result[name][f"non_null_{sc}"] = df[sc].dropna().shape[0]
        return result
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    files = ["cancer.xlsx", "eye_irritation.xlsx", "skin_sensitization.xlsx", "dart.xlsx"]
    for file in files:
        path = os.path.join(r"c:\Users\DS\Downloads\기말 data 선정", file)
        print(f"\n========================================\nFile: {file}")
        if os.path.exists(path):
            sheets_info = inspect_xlsx_sheets(path)
            if "error" in sheets_info:
                print("Error reading file:", sheets_info["error"])
            else:
                for sname, info in sheets_info.items():
                    print(f"  Sheet: {sname}")
                    print(f"    Shape: {info['shape']}")
                    print(f"    SMILES columns: {info['smiles_cols']}")
                    for k, v in info.items():
                        if k.startswith("non_null_"):
                            print(f"      {k}: {v}")
                    print(f"    Target candidates: {info['target_cols']}")
                    print(f"    Mixture counts: {info['mix_counts']}")
                    print(f"    Unique CASRN: {info['unique_cas']}, DTXSID: {info['unique_dtxsid']}, Chemical Name: {info['unique_name']}")
                    print(f"    Columns (up to 15): {info['columns']}")
        else:
            print("File does not exist at path:", path)
