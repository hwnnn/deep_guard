import 'package:flutter/services.dart' show rootBundle;
import 'dart:convert';

class AssetsManager {
  static Map<String, List<String>> assetsByFolder = {};

  /// 모든 Assets Manifest 로드 (앱 실행 시 1번만)
  static Future<void> loadAssetsMap() async {
    final manifestContent = await rootBundle.loadString('AssetManifest.json');
    final Map<String, dynamic> manifestMap = json.decode(manifestContent);

    assetsByFolder = {
      "test_images": [],
      "analyzing_icons": [],
      "analyzing_animations": [],
    };

    manifestMap.keys.forEach((path) {
      if (path.startsWith("assets/test_images/")) {
        assetsByFolder["test_images"]!.add(path);
      } else if (path.startsWith("assets/analyzing_icons/")) {
        assetsByFolder["analyzing_icons"]!.add(path);
      } else if (path.startsWith("assets/analyzing_animations/")) {
        assetsByFolder["analyzing_animations"]!.add(path);
      }
    });
  }

  /// 특정 파일명으로 찾기 (예: "successed.gif")
  static String? find(String filename) {
    for (var folder in assetsByFolder.values) {
      for (var path in folder) {
        if (path.endsWith(filename)) return path;
      }
    }
    return null;
  }
}
