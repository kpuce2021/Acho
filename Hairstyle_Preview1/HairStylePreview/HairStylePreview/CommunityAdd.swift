//
//  CommunityAdd.swift
//  HairStylePreview
//
//  Created by 곽재선 on 2021/05/10.
//

import UIKit

class CommunityAdd: UIViewController{
    
    @IBOutlet weak var addImage: UIImageView!
    @IBOutlet weak var addContent: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
    }
    
    @IBAction func addBtn(_ sender: UIButton) {
        cellContent.append(addContent.text!)
        if let controller = self.storyboard?.instantiateViewController(identifier: "Community") {
            self.navigationController?.pushViewController(controller, animated: true)
        }
    }
    
    
}
