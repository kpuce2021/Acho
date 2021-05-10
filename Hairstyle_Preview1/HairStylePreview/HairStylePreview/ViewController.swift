//
//  ViewController.swift
//  HairStylePreview
//
//  Created by 김정태 on 2021/04/05.
//
///메인

import UIKit


class ViewController: UIViewController {
    
    @IBOutlet var appTitle: UILabel!
    
    @IBOutlet var pictureBtn: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
    }
    @IBAction func btnExperience(_ sender: Any) {
        if let controller = self.storyboard?.instantiateViewController(identifier: "Camera") {
            self.navigationController?.pushViewController(controller, animated: true)
            
        }
        
    }
    
}
