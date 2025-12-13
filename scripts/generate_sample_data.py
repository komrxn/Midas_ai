"""
Generate sample data SQL file with hashed password.
Run this script to create sample_data.sql, then load it with:
    psql -U postgres -d accountant_db -f sample_data.sql
"""
import sys
from pathlib import Path

# Add parent directory to path to import from api
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from api.auth.jwt import get_password_hash
from api.utils.sample_data import generate_sample_data_sql


def main():
    print("🎲 Generating sample data...")
    
    # Hash the demo password
    password_hash = get_password_hash("demo123")
    
    # Generate SQL
    sql = generate_sample_data_sql(
        username="demo",
        email="demo@example.com",
        password_hash=password_hash
    )
    
    # Write to file
    output_file = Path(__file__).parent.parent.parent / "sample_data.sql"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(sql)
    
    print(f"✅ Sample data SQL generated: {output_file}")
    print(f"📊 Contains:")
    print(f"   - 1 demo user (username: demo, password: demo123)")
    print(f"   - ~270 transactions over 3 months")
    print(f"   - All 14 categories populated")
    print(f"\n💡 To load:")
    print(f"   psql -U postgres -d accountant_db -f sample_data.sql")


if __name__ == "__main__":
    main()
