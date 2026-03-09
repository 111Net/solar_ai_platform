import 'package:dio/dio.dart';

class ApiService {
  final Dio _dio = Dio(BaseOptions(
    baseUrl: "https://api.yourdomain.com"
  ));

  Future<Map<String, dynamic>> requestSolarPlan(Map data) async {
    final response = await _dio.post("/solar-plan", data: data);
    return response.data;
  }
}