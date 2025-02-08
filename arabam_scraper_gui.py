import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # To use combobox for page selection
from arabam_scraper import ArabamScraper  # ArabamScraper class
import threading  # Import the threading module

class ScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Arabam Scraper")
        self.root.geometry("400x400")
        self.root.minsize(400, 400)  # Set a minimum window size
        self.root.configure(bg="#f0f8ff")

        # Kategori
        self.category_label = tk.Label(root, text="Category:", bg="#f0f8ff", font=("Arial", 10, "bold"))
        self.category_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.category_entry = tk.Entry(root, font=("Arial", 10))
        self.category_entry.insert(0, "otomobil")  # Varsayılan değer
        self.category_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Min Price
        self.min_price_label = tk.Label(root, text="Min Price:", bg="#f0f8ff", font=("Arial", 10, "bold"))
        self.min_price_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.min_price_entry = tk.Entry(root, font=("Arial", 10))
        self.min_price_entry.insert(0, "0")  # Varsayılan değer
        self.min_price_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Max Price
        self.max_price_label = tk.Label(root, text="Max Price:", bg="#f0f8ff", font=("Arial", 10, "bold"))
        self.max_price_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.max_price_entry = tk.Entry(root, font=("Arial", 10))
        self.max_price_entry.insert(0, "100000000")  # Varsayılan değer
        self.max_price_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Output File Name
        self.output_label = tk.Label(root, text="Output File Name:", bg="#f0f8ff", font=("Arial", 10, "bold"))
        self.output_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.output_entry = tk.Entry(root, font=("Arial", 10))
        self.output_entry.insert(0, "InformationsOutput")  # Varsayılan değer
        self.output_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Max Pages
        self.max_pages_label = tk.Label(root, text="Max Pages:", bg="#f0f8ff", font=("Arial", 10, "bold"))
        self.max_pages_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        # Dropdown for selecting max pages (1-50)
        self.max_pages_combo = ttk.Combobox(root, values=list(range(1, 51)), state="readonly", width=5, font=("Arial", 10))
        self.max_pages_combo.set(2)  # Default value
        self.max_pages_combo.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        # Start Button
        self.start_button = tk.Button(root, text="Start Scraping", command=self.start_scraping, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.start_button.grid(row=5, column=0, columnspan=2, pady=20)

        # Configure the grid to expand properly
        root.grid_columnconfigure(1, weight=1)

    def start_scraping(self):
        try:
            category = self.category_entry.get()
            min_price = int(self.min_price_entry.get())
            max_price = int(self.max_price_entry.get())
            output_file_name = self.output_entry.get() + ".csv"
            max_pages = int(self.max_pages_combo.get())

            # Run the scraper in a separate thread to keep the GUI responsive
            scraper_thread = threading.Thread(target=self.run_scraper, args=(category, min_price, max_price, output_file_name, max_pages))
            scraper_thread.start()

        except Exception as e:
            # Display an error message if any exception occurs
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def run_scraper(self, category, min_price, max_price, output_file_name, max_pages):
        try:
            scraper = ArabamScraper(
                category=category,
                min_price=min_price,
                max_price=max_price,
                output_file_name=output_file_name,
                max_pages=max_pages
            )
            
            scraper.scrape()
            messagebox.showinfo("Success", "Scraping finished successfully!")

        except Exception as e:
            # Display an error message if any exception occurs during scraping
            messagebox.showerror("Error", f"An error occurred while scraping: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    gui = ScraperGUI(root)
    root.mainloop()
