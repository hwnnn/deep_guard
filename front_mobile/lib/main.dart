import 'package:flutter/material.dart';
import 'Screens/LandingPage.dart';
import 'Routers/routing_point.dart';
import 'Utils/asset_managers.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await dotenv.load(fileName: '.env');
  await AssetsManager.loadAssetsMap();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    // 서버 약관 동의 플래그 저장 여부에 따라 랜딩페이지 설정
    return MaterialApp(
      title: 'DeepGuard',
      debugShowCheckedModeBanner: false,
      initialRoute: RoutingPoint.landing,   // initial routing point
      home: const LandingPage(title: 'DeepGuard'),
    );
  }
}