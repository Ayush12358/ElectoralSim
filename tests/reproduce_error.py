import polars as pl
import numpy as np

def reproduce():
    # Attempt to reproduce AgentSet.add logic
    df_empty = pl.DataFrame()
    
    new_agents = pl.DataFrame({
        "name": ["A", "B"],
        "val": [1, 2]
    })
    
    # Add unique_id
    new_agents = new_agents.with_columns(
        pl.Series(np.random.randint(0, 100, 2)).alias("unique_id")
    )
    
    print("New Agents columns:", new_agents.columns)
    
    # Concat
    try:
        res = pl.concat([df_empty, new_agents], how="diagonal_relaxed")
        print("Concat successful. Columns:", res.columns)
    except Exception as e:
        print(f"Concat failed: {e}")

if __name__ == "__main__":
    reproduce()
