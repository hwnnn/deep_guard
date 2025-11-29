import 'package:dio/dio.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

final HOST = dotenv.env['HOST'];
/// taskid == /taskid, if null, just sned taskid to ''
Future<Map<String, dynamic>> requestToServer(
      {
        String? taskid,
        required String endpoint,
        required String type,
        required Map<String, dynamic> data,
        required Map<String, String> headers
      }
    ) async {
        final dio = Dio();
        final String requestURL = 'http://$HOST:8000' + endpoint + taskid!;  // 디버깅용 localhost -> 10.0.2.2
        try {
          final response;
          if (type == 'POST'){
            response = await dio.post(
              requestURL, // 👉 백엔드 API 주소
              data: FormData.fromMap(data),
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
          else{
            print('POST, GET 요청 중 하나를 선택해주세요');
            return {};
          }
          return response.data;
        } catch (e) {
          print(e);
          return {};
        }
}