# Dynamic DataTable with Django & DataTables.js

This project is a **dynamic, server-side DataTable** implementation using **Django (backend)** and **jQuery DataTables.js (frontend)**. It supports:

- **Dynamic model selection** (fetch data from different Django models)
- **Server-side processing** (fast performance on large datasets)
- **Multi-select filtering** using **Select2.js**
- **Live search and sorting**
- **Exporting data** (CSV, Excel, PDF)

---

## 🚀 Features

- **Django backend API** that serves paginated, filterable, and sortable data dynamically.
- **Frontend DataTable** that supports:
  - Column sorting
  - Server-side filtering
  - Multi-select dropdown filters (using Select2)
  - Search across multiple columns
  - Export to CSV, Excel, and PDF
- **Dynamic model selection**: API can serve different models by specifying a parameter.

---

## 🛠 Setup Instructions

### **1️⃣ Clone the Repository**
```sh
git clone <your-repo-url>
cd <your-project-folder>
```

### **2️⃣ Create & Activate a Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate     # On Windows
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Apply Migrations**
```sh
python manage.py migrate
```

### **5️⃣ Load Sample Data (Optional)**
If you have a fixture file:
```sh
python manage.py loaddata sample_data.json
```

### **6️⃣ Run the Server**
```sh
python manage.py runserver
```

The app will be available at **http://127.0.0.1:8000**

---

## 📂 Project Structure

```
📦 your-project
│── 📂 datatable_app      # Django app
│   │── 📂 migrations     # Django migrations
│   │── models.py         # Database models (Product, Order, etc.)
│   │── views.py          # Django views serving DataTables API
│   │── urls.py           # URL routes
│   │── templates/        # HTML templates
│── 📂 static             # Static files (CSS, JS)
│── 📂 templates          # Frontend UI templates
│── manage.py             # Django management commands
│── requirements.txt      # Python dependencies
│── README.md             # You're reading it now!
```

---

## 🔌 API Endpoints

### **1️⃣ Get Table Data**
#### **URL: `/api/data/`**
**Method:** `GET`

| Parameter      | Description                        | Example         |
|---------------|------------------------------------|----------------|
| `model`       | Name of the Django model          | `Product`      |
| `searchValue` | Global search term                | `Chair`        |
| `orderColumn` | Column index for sorting          | `2`            |
| `orderDir`    | Sorting direction (`asc`/`desc`)  | `desc`         |
| `start`       | Offset for pagination             | `0`            |
| `length`      | Number of records per page        | `10`           |

**Response Example:**
```json
{
  "draw": 1,
  "recordsTotal": 100,
  "recordsFiltered": 50,
  "data": [
    {
      "id": 1,
      "name": "Chair",
      "category": "Furniture",
      "price": 150.0,
      "stock": 80,
      "created_at": "2025-02-07T00:26:16.410Z"
    }
  ]
}
```

---

## 🖥️ **Frontend Configuration**

The frontend is powered by **jQuery DataTables.js** and **Select2.js**.

### **1️⃣ Table Initialization**
Located in **`index.html`**:
```js
const tablesConfig = [
    {
        "tableId": "dynamicTable",
        "api_url": "/api/data/",
        "model": "Product",
        "filters": [{ "field": "category", "label": "Category", "type": "multi-select" }]
    },
];

$(document).ready(function () {
    tablesConfig.forEach(config => fetchModelColumns(config));
});
```

### **2️⃣ Handle Filters**
```js
config.filters.forEach(filter => {
    $(`#${filter.field}Filter`).on('change', function () {
        console.log(`🎛 Filter '${filter.field}' Changed`);
        table.ajax.reload();
    });
});
```

---

## 🚀 Deploying to Production

### **1️⃣ Setup Gunicorn & Static Files**
```sh
pip install gunicorn
python manage.py collectstatic
```

### **2️⃣ Run Gunicorn**
```sh
gunicorn your_project.wsgi:application --bind 0.0.0.0:8000
```

### **3️⃣ Configure Nginx (If Hosting)**
Add this to `/etc/nginx/sites-available/your_project`
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path-to-your-project/static/;
    }
}
```
Then restart Nginx:
```sh
sudo systemctl restart nginx
```

---

## 📜 Git Setup & Ignoring Files

### **1️⃣ Initialize Git Repo**
```sh
git init
git add .
git commit -m "Initial commit"
```

### **2️⃣ Set Remote & Push**
```sh
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

### **3️⃣ Ignore Unwanted Files**
Create a `.gitignore` file:
```
# Ignore system files
.DS_Store
Thumbs.db

# Ignore Python virtual environment
venv/
__pycache__/

# Ignore database files
*.sqlite3

# Ignore static & node_modules
staticfiles/
node_modules/
```

---

## 🎯 **Next Steps**
- ✅ Implement user authentication
- ✅ Add more filters dynamically
- ✅ Improve UI/UX with TailwindCSS or Bootstrap
- ✅ Deploy on AWS/GCP

---

## 📞 Need Help?
Feel free to open an **issue** or reach out! 🚀🔥

