import 'package:flutter/material.dart';
import '../Bars/header_footer.dart';
import '../Routers/routing_point.dart';
import '../Bars/navigation.dart';
import '../Widgets/elevated_button.dart';
import '../Widgets/reusable_widgets.dart';
import '../Utils/asset_managers.dart';

class UploadPage extends StatefulWidget {
  const UploadPage({super.key});

  @override
  State<UploadPage> createState() => _UploadPageState();
}

class _UploadPageState extends State<UploadPage> {
  ImageProvider? origImage;
  ImageProvider? dfImage;
  bool enableBack = false;
  bool enableHelp = true;
  // 업로드 전/후 상태
  bool get hasOrigImage => origImage != null;
  bool get hasDfImage => dfImage != null;

  // AssetManager를 통한 애셋 자동 로드 (이미지 요청 성공 확인 후 사용자 갤러리에서 업로드하면 어셋 디렉터리의 test_images 디렉터리에 캐싱하는 방식으로 수정 예정)
  // 일단 시연할 때 디버깅 돌리는 상황 한정으로 존재하면 됨
  final testOrig = AssetsManager.find('testOrig.png');
  final testDeep = AssetsManager.find('testDeep.png');

  // 업로드 버튼 클릭 시 호출될 함수 (더미 처리)
  void _pickOrigImage() {
    setState(() {
      enableBack = true;
      origImage = AssetImage(testOrig ?? ""); // TODO: 이미지 선택 로직
    });
  }

  void _pickDfImage() {
    setState(() {
      enableBack = true;
      dfImage = AssetImage(testDeep ?? ""); // TODO: 이미지 선택 로직
    });
  }

  void _onBack() {
    setState(() {
      this.enableBack = false;
      this.origImage = null;
      this.dfImage = null;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: DeepGuardHeader(
        showBack: this.enableBack,
        showHelp: this.enableHelp,
        onBack: _onBack
      ),
      backgroundColor: Colors.white,
      bottomNavigationBar: BottomNavBar(
        selectedIndex: 0,
        onTap: (i) {},
      ),

      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 18),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              // 1. 타이틀
              const TitleSection(
                mainTitle: "Upload Media",
                subTitle: "Detect deepfakes with AI",
              ),

              const SizedBox(height: 10),

              // 2. 이미지 박스 2개 (업로드 전/후 자동 전환)
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  ImageBox(
                    title: "Orig Image",
                    description: "Upload a Orig image or video",
                    uploadedImage: origImage,
                    onUploadTap: _pickOrigImage,
                  ),
                  ImageBox(
                    title: "DF Image",
                    description: "Upload a DF image or video",
                    uploadedImage: dfImage,
                    onUploadTap: _pickDfImage,
                  ),
                ],
              ),

              const SizedBox(height: 200),

              // 2. 가이드 안내 버튼
              CustomElevatedButton(
                text: "Tool Guidance",
                textColor: Colors.white,
                fontSize: 16,
                backgroundColor: Colors.blue, // 비활성화 색
                width: MediaQuery.of(context).size.width * 0.5,
                padding: EdgeInsets.all(0),
                onPressed: () {}
              ),

              const SizedBox(height: 30),

              // 3. Detection 버튼 (둘 다 업로드되어야 활성화)
              CustomElevatedButton(
                text: "Start Detection",
                textColor: Colors.white,
                fontSize: 16,
                backgroundColor: (hasOrigImage && hasDfImage)
                    ? Colors.blue
                    : Colors.grey, // 비활성화 색
                width: MediaQuery.of(context).size.width * 0.85,
                onPressed: (hasOrigImage && hasDfImage)
                    ? () {
                  Navigator.push(
                    context,
                    RoutingPoint.generateRoute(
                      settings: const RouteSettings(
                        name: RoutingPoint.detecting,
                      ),
                    ),
                  );
                }
                    : null,
              ),

              const SizedBox(height: 40),
            ],
          ),
        ),
      ),
    );
  }
}