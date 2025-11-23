import 'package:dio/dio.dart';
import 'package:flutter/material.dart';

Future<Map<String, dynamic>> requestToServer(String endpoint, String type, Map<String, dynamic> data, Map<String, String> headers) async {
  final dio = Dio();
  final String requestURL = 'http://localhost:8000' + endpoint;
  try {
    Response<dynamic> response = new Response(
        requestOptions: RequestOptions()
    );
    
    if (type == 'POST'){
      response = await dio.post(
        requestURL, // 👉 백엔드 API 주소
        data: data,
        options: Options(
            headers: headers
        ),
      );
    }
    else if (type == 'GET'){
      response = await dio.get(
        requestURL, // 👉 백엔드 API 주소
        data: data,
        options: Options(
            headers: headers
        ),
      );
    }

    Map<String, dynamic> responsedata = response.data;
    return responsedata;
  } catch (e) {
    return {};
  }
}