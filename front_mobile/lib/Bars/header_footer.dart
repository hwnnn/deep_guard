import 'package:flutter/material.dart';

// 생성자 생성 -> 빌드, preferredSize
class DeepGuardHeader extends StatelessWidget implements PreferredSizeWidget {
  final bool showBack;
  final bool showHelp;
  final VoidCallback? onBack;

  const DeepGuardHeader({
    super.key,
    this.showBack = false,  // 파라미터 기본값
    this.showHelp = false,
    this.onBack,
  });    // 헤더 생성자 생성
  @override
  Widget build(BuildContext context) {
    return AppBar(
      automaticallyImplyLeading: false,
      backgroundColor: Colors.white,
      elevation: 0,
      centerTitle: true,

      // 뒤로 가기 (leading - 제목의 왼쪽 UI 구성)
      leading: this.showBack
          ? IconButton(
        icon: const Icon(Icons.arrow_back_ios, color: Colors.black),
        // onPressed: onBack ?? () => Navigator.pop(context),
        onPressed: onBack
      )
          : const SizedBox.shrink(),    // 빈 위젯을 반환할 때 사용

      // 제목
      title: const Text(
        'DeepFake Detector',
        style: TextStyle(
          fontSize: 20,
          fontWeight: FontWeight.bold,
          color: Colors.black,
        ),
      ),

      // 도움말 버튼 (actions - 툴바 오른쪽의 위젯 리스트)
      actions: [
        this.showHelp
            ? IconButton(
          icon: const Icon(Icons.help_outline, color: Colors.black),
          onPressed: () {
            // TODO: 도움말 페이지 이동 구현 예정
          },
        )
            : const SizedBox.shrink(),
      ],
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);
}
