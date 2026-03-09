useEffect(() => {
  fetch("/admin/metrics")
    .then(res => res.json())
    .then(data => setMetrics(data));
}, []);