//
//  PreviewViewController.swift
//  NBATikTok
//
//  Created by RandyLiu on 20/8/2020.
//  Copyright © 2020 h-tamader-team/RandyLiu. All rights reserved.
//

import UIKit
import AVFoundation

class PreviewViewController: UIViewController {
    // Status
    private enum ProcessVideoStatus {
        case noVideo
        case recorded
        case uploading
        case uploaded
        case processing
        case processed
    }
    
    // Declare variables
    @IBOutlet weak var uploadButton: UIButton!
    @IBOutlet weak var previewView: PreviewView!
    @IBOutlet weak var statusLabel: UILabel!
    var playerLayer: AVPlayerLayer?
    public var videoURL: URL?
    private var videoProcessStatus: ProcessVideoStatus = .noVideo
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Change button style
        uploadButton.layer.cornerRadius = 10
        
        // Change status label style
        statusLabel.layer.cornerRadius = 30
        statusLabel.isHidden = true

        // Do any additional setup after loading the view.
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(true)
        
        // Play preview video and loop
        DispatchQueue.main.async {
            self.videoProcessStatus = .recorded
            let player = AVPlayer(url: self.videoURL!)
            
            NotificationCenter.default.addObserver(forName: .AVPlayerItemDidPlayToEndTime, object: player.currentItem, queue: nil) { (_) in
                        player.seek(to: CMTime.zero)
                        player.play()
            }
            
            self.playerLayer = AVPlayerLayer(player: player)
            self.playerLayer!.frame = self.previewView.bounds
            self.previewView!.layer.addSublayer(self.playerLayer!)
            player.play()
        }
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        cleanup(outputFileURL: self.videoURL!)
    }
    
    func cleanup(outputFileURL: URL) {
        let path = outputFileURL.path
        if FileManager.default.fileExists(atPath: path) {
            do {
                try FileManager.default.removeItem(atPath: path)
            } catch {
                print("Could not remove file at url: \(outputFileURL)")
            }
        }
    }
    
    // Upload video to database
    @IBAction func uploadVideo(_ sender: UIButton) {
        self.videoProcessStatus = .uploading
        
//        self.statusLabel.isHidden = false
//        self.statusLabel.text = "Uploading..."
//        let spinnerView = SpinnerView()
        let screenSize: CGRect = UIScreen.main.bounds
        let spinnerView = SpinnerView(frame: CGRect(x: screenSize.width/2 - 50, y: screenSize.height/2 - 50, width: 100, height: 100))
        self.view.addSubview(spinnerView)
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
