import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.animation import FuncAnimation


# =======================================
# Load csv data
# =======================================
print("="*100)
print("Loading CSV data...")
try:
    global df
    file_path = "data/T1.csv"
    df = pd.read_csv(file_path)

    df['Date/Time'] = pd.to_datetime(
        df['Date/Time'],
        format='%d %m %Y %H:%M',
        errors='coerce'
    )
    print("CSV file loaded successfully")
except Exception as e:
    print(f"Error loading CSV file: {e}")
    df = pd.DataFrame()  # Create empty DataFrame to prevent further errors


# =======================================
# Filtering data by month
# =======================================
def csv_data_chunk(month=7):
    # Filter rows for the selected month and year
    print("="*100)
    print("Filtering data by month and cleaning...")
    global df
    try:
        df = df[
            (df['Date/Time'].dt.month == month)
        ]

        months = [
            "January", "February", "March", 
            "April", "May", "June", "July", 
            "August", "September", "October", 
            "November", "December"
        ]

        global month_name
        month_name = months[month - 1]

        print(f"Data filtered for month {month_name} successfully")

    except Exception as e:
        print(f"Error filtering data by month: {e}")


# =======================================
# Data Cleaning
# =======================================
def clean_data():
    # =======================================
    # Detect and Handle Missing/Null Values
    # =======================================
    global df
    print("="*100)
    print("Detecting and handling missing/null values...")
    # Fill missing values automatically
    try:
        for column in df.columns:

            # If numeric column → fill with mean
            if pd.api.types.is_numeric_dtype(df[column]):
                df[column] = df[column].fillna(df[column].mean())

            # If text column → fill with mode
            else:
                df[column] = df[column].fillna(df[column].mode()[0])
        print("Missing/null values handled successfully")
    except Exception as e:
        print(f"Error handling missing/null values: {e}")

    # =======================================
    # Remove Duplicate Records
    # =======================================
    print("="*100)
    print("Removing duplicate records...")

    try:
        df = df.drop_duplicates()
        print("Duplicate records removed successfully")
    except Exception as e:
        print(f"Error removing duplicate records: {e}")

    # =======================================
    # Correct Corrupted Data Types
    # =======================================
    print("="*100)
    print("Correcting corrupted data types...")
    # Try converting object columns into numeric if possible
    try:    
        for column in df.columns:
            if df[column].dtype == "object":

                # Remove unwanted spaces
                df[column] = df[column].astype(str).str.strip()

                # Attempt numeric conversion
                converted = pd.to_numeric(df[column], errors='coerce')

                # If many values successfully convert, replace column
                if converted.notnull().sum() > len(df[column]) * 0.5:
                    df[column] = converted

        output_file = "data/T1_cleaned.csv"
        df.to_csv(output_file, index=True)
        print(f"Data filtered and cleaned successfully")
    except Exception as e:
        print(f"Error correcting corrupted data types: {e}")


# =======================================
# Descriptive Statistics
# =======================================
def descriptive_statistics():
    global df
    print("="*100)
    print("Generating descriptive statistics...")
    global columns
    columns = [
        "LV ActivePower (kW)",
        "Wind Speed (m/s)",
        "Theoretical_Power_Curve (KWh)",
        "Wind Direction (°)"
    ]

    try:
        data = []
        for column in columns:
            if column not in df.columns:
                continue
            series = df[column]
            data.append([
                round(series.mean(), 2),
                round(series.median(), 2),
                round(series.mode().iloc[0] if not series.mode().empty else np.nan, 2),
                round(series.std(), 2),
                round(series.var(), 2)
            ])

        fig, ax = plt.subplots(figsize=(6, 2.5))
        plt.title(f"Descriptive Statistic of DataFrame for {month_name}", fontsize=12, pad=10)
        ax.axis("tight")
        ax.axis("off")

        table = ax.table(
            cellText=data,
            rowLabels=columns,
            colLabels=["Mean", "Median", "Mode", "Standard deviation", "Variance"],
            loc="center"
        )
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.6, 2)

        output_dr = "outputs/"
        if not os.path.exists(output_dr):
            os.makedirs(output_dr)

        plt.savefig(
            f"outputs/descriptive_statistic_of_dataframe_for_{month_name}.png",
            bbox_inches='tight',
        )
        plt.close()
        print(f"'descriptive_statistic_of_dataframe_for_{month_name}.png' created and saved in the 'outputs' folder.")
    except Exception as e:
        print(f"Error generating descriptive statistics: {e}")

# =======================================
# Distribution Analysis
# =======================================
def distribution_analysis():
    print("="*100)
    print("Generating distribution analysis...")
    try:
        for col in columns:
            if col not in df.columns:
                print(f"Column '{col}' not found.")
                continue

            # Plot histogram
            plt.figure(figsize=(6, 4))
            plt.hist(df[col], bins=10)

            plt.title(f"Distribution of {col} for {month_name}", fontsize=12, pad=10)
            plt.xlabel(col)
            plt.ylabel("Frequency")

            # Save each plot as PNG
            output_dr = "outputs/distribution_analysis/"
            if not os.path.exists(output_dr):
                os.makedirs(output_dr)
            save_col = col.replace("/", " per ") if col == "Wind Speed (m/s)" else col
            plt.savefig(f"outputs/distribution_analysis/distribution_{save_col}_for_{month_name}.png", dpi=300, bbox_inches='tight')
            plt.close()

            print(f"'distribution_{save_col}_for_{month_name}.png' created and saved in the 'outputs/distribution_analysis' folder.")
    except Exception as e:
        print(f"Error generating distribution analysis: {e}")

# =======================================
# Correlation Analysis
# =======================================
def correlation_analysis():
    global df
    print("="*100)
    print("Generating correlation analysis...")
    try:
        # Keep only numeric columns
        numeric_df = df.select_dtypes(include="number")

        # Correlation matrix
        corr = numeric_df.corr()

        # Plot heatmap
        plt.figure(figsize=(8, 6))

        ax = sns.heatmap(
            corr,
            annot=True,
            fmt=".2f",
            cmap="Blues",
            vmin=-1,
            vmax=1,
            linewidths=0.5
        )

        plt.title(f"Correlation Heatmap for {month_name}", fontsize=12, pad=10)

        # Rotate x-axis labels
        plt.xticks(rotation=45, ha="right")

        # Output directory for heatmap
        output_dr = "outputs/correlation_analysis/"
        if not os.path.exists(output_dr):
            os.makedirs(output_dr)

        # Save as PNG
        plt.savefig(f"outputs/correlation_analysis/correlation_heatmap_for_{month_name}.png", dpi=300, bbox_inches="tight")
        plt.close()

        print(f"'correlation_heatmap_for_{month_name}.png' created and saved in the 'outputs/correlation_analysis' folder.")

        for i, col in enumerate(columns):
            x_col = numeric_df.columns[i] 
            i = 0 if i + 1 >= len(columns) else i 
            y_col = numeric_df.columns[i + 1]  
            # Calculate correlation
            correlation = numeric_df[x_col].corr(numeric_df[y_col])

            # Create scatterplot
            plt.figure(figsize=(8, 5))

            sns.scatterplot(
                data=numeric_df,
                x=x_col,
                y=y_col
            )

            # Add title and labels
            plt.title(f"{x_col} vs {y_col}\nCorrelation = {correlation:.2f}")
            plt.xlabel(x_col)
            plt.ylabel(y_col)

            # Save plot
            output_dr = "outputs/correlation_analysis/correlation_scatterplots/"
            if not os.path.exists(output_dr):
                os.makedirs(output_dr)

            if x_col == "Wind Speed (m/s)":
                x_col = x_col.replace("/", " per ")
            elif y_col == "Wind Speed (m/s)":
                y_col = y_col.replace("/", " per ")
            
            plt.savefig(
                f"outputs/correlation_analysis/correlation_scatterplots/correlation_scatterplot_{x_col}_vs_{y_col}_for_{month_name}.png",
                dpi=300,
                bbox_inches="tight"
            )
            plt.close()

            print(f"'correlation_scatterplot_{x_col}_vs_{y_col}_for_{month_name}.png' saved in the 'outputs/correlation_analysis/correlation_scatterplots' folder.")
    except Exception as e:
        print(f"Error generating correlation analysis: {e}")


# =======================================
# Comparative Analysis
# =======================================
def comparative_analysis():
    print("="*100)
    print("Generating comparative analysis...")
    df['Day'] = df['Date/Time'].dt.date     

    category_col = "Day"
    grouped = df.groupby(category_col)[columns].mean()
    try:
        for col in columns:
            fig, ax = plt.subplots(figsize=(10, 6))

            # Plot bars with lower zorder so the line appears on top
            grouped[col].plot(kind="bar", ax=ax, color="#69b3a2", alpha=0.85, zorder=2)

            # Plot trend line using integer x positions to align with bar locations
            x = np.arange(len(grouped))
            y = grouped[col].values
            ax.plot(
                x,
                y,
                color="#ff7f0e",
                marker="o",
                markersize=6,
                linewidth=2.2,
                label="Trend Line",
                zorder=3
            )

            # Ensure ticks align with bars and show readable labels
            ax.set_xticks(x)
            ax.set_xticklabels([str(d) for d in grouped.index], rotation=45, ha='right')

            ax.set_title(f"Mean Comparison of {col} by {category_col} for {month_name}", fontsize=14, pad=12)
            ax.set_xlabel(category_col)
            ax.set_ylabel("Mean Value")
            ax.legend(loc="upper left")
            ax.grid(axis="y", alpha=0.25)

            # Save chart
            output_dr = "outputs/comparative_analysis/"
            if not os.path.exists(output_dr):
                os.makedirs(output_dr)
            save_col = col.replace("/", " per ") if col == "Wind Speed (m/s)" else col
            fig.savefig(f"outputs/comparative_analysis/mean_comparison_of_{save_col}_by_{category_col}_for_{month_name}.png", dpi=300, bbox_inches='tight')
            plt.close(fig)

            print(f"'mean_comparison_of_{save_col}_by_{category_col}_for_{month_name}.png' created and saved in the 'outputs/comparative_analysis' folder.")
    except Exception as e:
        print(f"Error generating comparative analysis: {e}")

# =======================================
# Create animation of Scatterplot
# =======================================
def anim_plot():
    try:
        for i, col in enumerate(columns):
            # Columns
            x_col = df.columns[i]
            i = 0 if i + 1 >= len(columns) else i
            y_col = df.columns[i + 1]

            # Create figure
            fig, ax = plt.subplots(figsize=(8, 5))

            # Animation function
            def update(frame):
                ax.clear()

                # Plot data up to current frame
                current_data = df.iloc[:frame + 1]

                ax.scatter(
                    current_data[x_col],
                    current_data[y_col]
                )

                ax.set_title("Wind Speed vs Power Output Over Time")
                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)

            # Create animation
            ani = FuncAnimation(
                fig,
                update,
                frames=len(df),
                interval=100,
                repeat=False
            )

            # Save animation
            output_dr = "outputs/comparative_analysis/animated_scatter/"
            if not os.path.exists(output_dr):
                os.makedirs(output_dr)
            ani.save(
                f"outputs/comparative_analysis/animated_scatter/animated_scatter_{x_col}_vs_{y_col}.gif", 
                writer="pillow")

            plt.close()

            print(f"Saved as 'animated_scatter_{x_col}_vs_{y_col}.gif' in the 'outputs/comparative_analysis/animated_scatter' folder.")
    except Exception as e:
        print(f"Error generating animated analysis: {e}")