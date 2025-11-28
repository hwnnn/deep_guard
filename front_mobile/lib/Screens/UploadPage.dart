import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
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
  bool enableBack = false;
  bool enableHelp = true;

  // 업로드 전/후 상태
  XFile? uploadImage;
  bool get hasImage => uploadImage != null;

  // 업로드 버튼 클릭 시 호출될 함수
  void _pickUploadImage() async {
    final uploadImage = await ImagePicker().pickImage(source: ImageSource.gallery);
    setState(() {
      this.uploadImage = uploadImage; // TODO: 이미지 선택 로직
      this.enableBack = true;
    });
  }

  void _onBack() {
    setState(() {
      this.enableBack = false;
      this.uploadImage = null;
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

      body: Container(
        alignment: Alignment.center,
        child: SingleChildScrollView(
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

                ImageBox(
                  title: "Image",
                  description: "Upload a Suspicious Image or Video",
                  uploadedImage: uploadImage,
                  onUploadTap: _pickUploadImage,
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
                  backgroundColor: (hasImage)
                      ? Colors.blue
                      : Colors.grey, // 비활성화 색
                  width: MediaQuery.of(context).size.width * 0.85,
                  onPressed: (hasImage)
                      ? () {
                    Navigator.push(
                      context,
                      RoutingPoint.generateRoute(
                        settings: const RouteSettings(
                          name: RoutingPoint.detecting,
                        ),
                        uploadedImage: this.uploadImage
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
      )
    );
  }
}