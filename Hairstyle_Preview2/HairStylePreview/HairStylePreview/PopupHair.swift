//
//  PopupHair.swift
//  HairStylePreview
//
//  Created by 곽재선 on 2021/05/09.
//

import UIKit

class PopupHair: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }
    @IBAction func selectLongHair(_ sender: Any) {
        let vcName = self.storyboard?.instantiateViewController(withIdentifier: "SelectImage")
        vcName?.modalTransitionStyle = .coverVertical
        self.present(vcName!, animated: true, completion: nil)
        //if let controller = self.storyboard?.instantiateViewController(identifier: "SelectImage") {
        //    self.navigationController?.pushViewController(controller, animated: true)
        //}
        
    }
    
    @IBAction func cancelPopup(_ sender: Any) {
        self.dismiss(animated: false, completion: nil)
    }
}
