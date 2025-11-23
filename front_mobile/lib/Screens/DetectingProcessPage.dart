import 'package:flutter/material.dart';
import '../Bars/header_footer.dart';
import '../Bars/navigation.dart';
import '../Widgets/elevated_button.dart';
import '../Routers/routing_point.dart';
import '../Utils/asset_managers.dart';

class DetectingPage extends StatelessWidget{

  const DetectingPage({super.key});

  Widget build(BuildContext context){
    final analyzingicon = AssetsManager.find('analyzing.png');

    return Scaffold(
      appBar: DeepGuardHeader(
        showBack: false,
        showHelp: false,
        onBack: (){},
      ),
      backgroundColor: Colors.white,

      body: Container(
        alignment: Alignment.center,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            const SizedBox(height: 60),
            const Text(
              'Analyzing...',
              style: TextStyle(
                fontSize: 48,
                fontWeight: FontWeight.bold,
                color: Colors.black,
              ),
            ),
            const SizedBox(height: 60),
            Image(
              image: AssetImage(analyzingicon ?? ""),
            ),
            CustomElevatedButton(
                text: 'Debuggingtest',
                textColor: Colors.white,
                fontSize: 16,
                backgroundColor: Colors.blue,
                width: MediaQuery.sizeOf(context).width * 0.5,
                onPressed: (){
                  Navigator.push(
                    context,
                    RoutingPoint.generateRoute(
                        settings: const RouteSettings(
                            name: RoutingPoint.detectionsuccessed
                        )
                    )
                  );
                }
            )
          ],
        )
      )
    );
  }
}

class DetectionSuccessedPage extends StatelessWidget{

  const DetectionSuccessedPage({super.key});

  Widget build(BuildContext context){

    final successGif = AssetsManager.find('successed.gif');

    return Scaffold(
        appBar: DeepGuardHeader(
          showBack: false,
          showHelp: false,
          onBack: (){},
        ),
        backgroundColor: Colors.white,

        body: Container(
            alignment: Alignment.center,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                const SizedBox(height: 60),
                const Text(
                  'Analyzing\nSuccessed',
                  style: TextStyle(
                    fontSize: 48,
                    fontWeight: FontWeight.bold,
                    color: Colors.black,
                  ),
                ),
                const SizedBox(height: 60),
                Image(
                  image: AssetImage(successGif ?? ""),
                ),
                CustomElevatedButton(
                    text: 'Show Report',
                    textColor: Colors.white,
                    fontSize: 16,
                    backgroundColor: Colors.blue,
                    width: MediaQuery.sizeOf(context).width * 0.5,
                    onPressed: (){
                      Navigator.push(
                          context,
                          RoutingPoint.generateRoute(
                              settings: const RouteSettings(
                                  name: RoutingPoint.detectionresult
                              )
                          )
                      );
                    }
                )
              ],
            )
        )
    );
  }
}

class DetectionFailedPage extends StatelessWidget{

  const DetectionFailedPage({super.key});

  Widget build(BuildContext context){

    final failedGif = AssetsManager.find('failed.gif');

    return Scaffold(
        appBar: DeepGuardHeader(
          showBack: false,
          showHelp: false,
          onBack: (){},
        ),
        backgroundColor: Colors.white,

        body: Container(
            alignment: Alignment.center,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                const SizedBox(height: 60),
                const Text(
                  'Analyzing\nFailed',
                  style: TextStyle(
                    fontSize: 48,
                    fontWeight: FontWeight.bold,
                    color: Colors.black,
                  ),
                ),
                const SizedBox(height: 60),
                Image(
                  image: AssetImage(failedGif ?? ""),
                ),
                CustomElevatedButton(
                    text: 'Retry',
                    textColor: Colors.white,
                    fontSize: 16,
                    backgroundColor: Colors.blue,
                    width: MediaQuery.sizeOf(context).width * 0.5,
                    onPressed: (){
                      Navigator.push(
                          context,
                          RoutingPoint.generateRoute(
                              settings: const RouteSettings(
                                  name: RoutingPoint.detecting
                              )
                          )
                      );
                    }
                )
              ],
            )
        )
    );
  }
}
