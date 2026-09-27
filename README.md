# ShopHub

ShopHub is a Django storefront with product search, session cart, and account registration/login.

## Deploy to Render

The root `render.yaml` Blueprint defines a Python web service and a PostgreSQL database. To create them:

1. Push the repository to GitHub.
2. In Render, choose **New → Blueprint** and connect `hammad-scripted/django-ecom` on the `main` branch.
3. Review the Blueprint resources and choose **Apply**.

Render installs `mysite/requirements.txt`, collects static files, applies database migrations, and loads the existing product catalog on the first deployment. Render generates the production `SECRET_KEY` automatically.

This configuration uses Render's free web and Postgres plans for a demo. Free web services sleep after 15 minutes of inactivity, and free Postgres databases expire after 30 days; upgrade the database before then to preserve registered accounts and store data. Product image uploads use the service filesystem, which is temporary on the free plan.
