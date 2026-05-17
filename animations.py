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