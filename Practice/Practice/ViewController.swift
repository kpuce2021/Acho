//
//  ViewController.swift
//  Practice
//
//  Created by 곽재선 on 2021/03/31.
//

import UIKit

class ViewController: UIViewController {
    
    
    @IBAction func clickLogin(_ sender: Any) {
        if let controller = self.storyboard?.instantiateViewController(identifier: "DetailController") {
            self.navigationController?.pushViewController(controller, animated: true)
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }


}

