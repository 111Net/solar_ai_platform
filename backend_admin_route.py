@app.get("/admin/metrics")
def get_metrics(db: Session = Depends(get_db)):

    total_customers = db.query(Customer).count()
    total_systems = db.query(SolarSystem).count()

    return {
        "total_customers": total_customers,
        "total_systems": total_systems
    }