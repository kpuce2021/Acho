//
//  SocialLogin.swift
//  HairStylePreview
//
//  Created by 곽재선 on 2021/04/06.
//

import UIKit

class SocialLogin: UIViewController {
    
    
    @IBAction func clickLogin(_ sender: Any) {
        if let controller = self.storyboard?.instantiateViewController(identifier: "UserInfo") {
            self.navigationController?.pushViewController(controller, animated: true)
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }


}
