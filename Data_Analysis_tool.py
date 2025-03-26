import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def load_data(file_path):
    """Loads the dataset and returns a DataFrame."""
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        print(f"File not found: {file_path}")
        return pd.DataFrame()  # Return an empty DataFrame if the file does not exist

def filter_data(df, filters):
    """Filters the dataset based on user input."""
    filtered_df = df.copy()

    for column, value in filters.items():
        if value and column in df.columns:
            filtered_df = filtered_df[filtered_df[column].astype(str).str.lower() == value.lower()]

    return filtered_df

def find_closest_matches(df, filters):
    """Finds and returns the closest matches based on the filters."""
    if df.empty:
        return pd.DataFrame()

    # Create a DataFrame to hold the differences
    differences = pd.DataFrame()

    for column, value in filters.items():
        if value and column in df.columns:
            # Calculate the absolute difference for numeric columns
            if pd.api.types.is_numeric_dtype(df[column]):
                differences[column] = abs(df[column] - float(value))
            else:
                # For non-numeric columns, we can use a simple string comparison
                differences[column] = df[column].astype(str).str.lower().apply(lambda x: 1 if x != value.lower() else 0)

    # Sum the differences to get a total score for each row
    differences['Total Difference'] = differences.sum(axis=1)

    # Get the closest matches (lowest total difference)
    closest_matches = df.loc[differences.nsmallest(5, 'Total Difference').index]

    return closest_matches

def visualize_data(df, x_column, y_column):
    """Generates a scatter plot showing the relationship between two columns."""
    if df.empty or x_column not in df.columns or y_column not in df.columns:
        print("No data to visualize or dataset missing required columns.")
        return

    x = df[x_column]
    y = df[y_column]

    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, marker='o', color='red', label="Data Points")
    
    # Calculate regression line using NumPy polyfit
    m, b = np.polyfit(x, y, 1)  
    plt.plot(x, m * x + b, linestyle='--', label="Regression Line", color='blue')

    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f"Scatter Plot of {y_column} vs {x_column}")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()

def main():
    file_path = input("Enter the file path of the CSV file: ")
    df = load_data(file_path)

    if df.empty:
        return  # Exit if the DataFrame is empty

    # Display the name of the columns
    print("Columns available for filtering:")
    columns = df.columns.tolist()
    for i, column in enumerate(columns):
        print(f"{i + 1}: {column}")

    # Ask user to select columns for filtering
    selected_columns = input("Enter the numbers of the columns you want to filter (comma-separated): ")
    selected_columns_indices = [int(x.strip()) - 1 for x in selected_columns.split(',') if x.strip().isdigit()]
    selected_columns = [columns[i] for i in selected_columns_indices if i < len(columns)]

    # Create a dictionary for filters
    filters = {}
    for column in selected_columns:
        value = input(f"Enter value for {column} (leave blank to skip): ").strip() or None
        filters[column] = value

    # Filter the data
    result = filter_data(df, filters)

    if result.empty:
        print("No exact matches found. Showing closest available options:")
        closest_matches = find_closest_matches(df, filters)
        print(closest_matches)
    else:
        print("Filtered Data:")
        print(result)

        # Ask user for columns to visualize
        x_column = input("Enter the column name for X-axis for visualization: ").strip()
        y_column = input("Enter the column name for Y-axis for visualization: ").strip()
        
        visualize_data(result, x_column, y_column)

if __name__ == "__main__":
    main()