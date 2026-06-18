import os
import pandas as pd

def inspect_endpoints(filepath, sheet_name):
    try:
        df = pd.read_excel(filepath, sheet_name=sheet_name)
        print(f"\n==================================================")
        print(f"File: {os.path.basename(filepath)} | Sheet: {sheet_name}")
        print(f"Total Rows: {len(df)}")
        
        # 1. Mixture column check
        mix_col = 'Mixture' if 'Mixture' in df.columns else None
        if mix_col:
            print("  Mixture counts:")
            print(df[mix_col].value_counts(dropna=False).head(5))
            
        # 2. Endpoint column check
        if 'Endpoint' in df.columns:
            print("  Endpoint counts:")
            print(df['Endpoint'].value_counts(dropna=False).head(10))
            
        # 3. Response and Response Unit check
        resp_cols = [c for c in df.columns if 'response' in c.lower() or 'level_of_evidence' in c.lower() or 'score' in c.lower()]
        for resp_col in resp_cols:
            print(f"  Response column: {resp_col}")
            null_count = df[resp_col].isna().sum()
            print(f"    Missing: {null_count}")
            # check types
            types = df[resp_col].dropna().apply(lambda x: type(x).__name__).value_counts()
            print("    Value types:")
            print(types)
            # Show top unique values
            print("    Top values:")
            print(df[resp_col].value_counts(dropna=False).head(5))
            
        # Check target candidates if they exist
        other_candidates = ['Level_of_Evidence', 'Tissue', 'Critical_Effect']
        for cand in other_candidates:
            if cand in df.columns:
                print(f"  Column: {cand}")
                print(df[cand].value_counts(dropna=False).head(5))

    except Exception as e:
        print("  Error:", str(e))

if __name__ == "__main__":
    targets = {
        "cancer.xlsx": ["Data"],
        "eye_irritation.xlsx": ["Data"],
        "skin_sensitization.xlsx": ["Data_invitro", "Data_invivo"],
        "dart.xlsx": ["Data"]
    }
    
    for file, sheets in targets.items():
        path = os.path.join(r"c:\Users\DS\Downloads\기말 data 선정", file)
        if os.path.exists(path):
            for sheet in sheets:
                inspect_endpoints(path, sheet)
        else:
            print("File does not exist at path:", path)
