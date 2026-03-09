ElevatedButton(
  onPressed: () async {
    final result = await ApiService().requestSolarPlan({
      "name": "Akin",
      "location": "Ibadan",
      "daily_kwh": 20,
      "monthly_income": 350000,
      "monthly_expenses": 180000
    });

    print(result);
  },
  child: Text("Generate Plan"),
)