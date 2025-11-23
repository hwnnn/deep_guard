import 'package:dio/dio.dart';

Future<Map<String, dynamic>> requestToServer(String endpoint, String type, Map<String, dynamic> data, Map<String, String> headers) async {
  final dio = Dio();
  final String requestURL = 'http://10.0.2.2:8000' + endpoint;  // 디버깅용 localhost -> 10.0.2.2
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
    return response.data;
  } catch (e) {
    return {};
  }
}