import 'package:flutter/material.dart';
import '../Bars/header_footer.dart';
import '../Routers/routing_point.dart';
import '../Bars/navigation.dart';
import '../Widgets/elevated_button.dart';
import '../Widgets/reusable_widgets.dart';

class UploadPage extends StatefulWidget {
  const UploadPage({super.key});

  @override
  State<UploadPage> createState() => _UploadPageState();
}

class _UploadPageState extends State<UploadPage> {
  ImageProvider? origImage;
  ImageProvider? dfImage;
  bool enableBack = false;
  // 업로드 전/후 상태
  bool get hasOrigImage => origImage != null;
  bool get hasDfImage => dfImage != null;

  // 업로드 버튼 클릭 시 호출될 함수 (더미 처리)
  void _pickOrigImage() {
    setState(() {
      enableBack = true;
      origImage = const AssetImage('assets/sample_orig.jpg'); // TODO: 이미지 선택 로직
    });
  }

  void _pickDfImage() {
    setState(() {
      enableBack = true;
      dfImage = const AssetImage('assets/sample_df.jpg'); // TODO: 이미지 선택 로직
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppHeader(
        showBack: enableBack,
        showHelp: false,
        onBack: (){
          setState(() {
            enableBack = false;
            origImage = null;
            dfImage = null;
          });
        },
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

              const SizedBox(height: 35),

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
                  // Navigator.push(
                  //   context,
                  //   RoutingPoint.generateRoute(
                  //     settings: const RouteSettings(
                  //       name: RoutingPoint.detectionResult,
                  //     ),
                  //   ),
                  // );
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