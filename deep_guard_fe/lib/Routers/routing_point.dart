import 'package:flutter/material.dart';

// 제작 페이지 등록
import '../Screens/LandingPage.dart';
import '../Screens/TermsAgreementPage.dart';

class RoutingPoint {
  // 앱 전체 route 이름 관리
  static const String landing = '/';
  static const String termsAgreement = '/terms';

  // route → 화면 위젯 빌더 매핑
  static Route<dynamic> generateRoute({required RouteSettings settings}) {
    switch (settings.name) {
      case landing:
        return MaterialPageRoute(
          builder: (_) => const LandingPage(title: 'DeepGuard'),
        );

      case termsAgreement:
        return MaterialPageRoute(
          builder: (_) => const TermsAgreementPage(),
        );

      default:
        return MaterialPageRoute(
          builder: (_) => const Scaffold(
            body: Center(
              child: Text('404 - Page not found'),
            ),
          ),
        );
    }
  }
}
