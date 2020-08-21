//
//  PreviewViewController.swift
//  NBATikTok
//
//  Created by RandyLiu on 20/8/2020.
//  Copyright © 2020 h-tamader-team/RandyLiu. All rights reserved.
//

import UIKit

class PreviewViewController: UIViewController {
    // Declare variables
    @IBOutlet weak var uploadButton: UIButton!
    public var testSegueText = ""
    
    override func viewDidLoad() {
        super.viewDidLoad()
        print(testSegueText)
        
        // Change button style
        uploadButton.layer.cornerRadius = 10

        // Do any additional setup after loading the view.
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
