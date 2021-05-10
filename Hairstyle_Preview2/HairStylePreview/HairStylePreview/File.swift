//
//  File.swift
//  HairStylePreview
//
//  Created by 김정태 on 2021/05/10.
//

import UIKit


var cellImage2 = ["3","6","1"]
var cellTitle2: Array<String> = ["ID 3","ID 1","ID 2"]
var cellContent2: Array<String> = ["새로 추가","어때요?","괜찮나요?"]



class File : UIViewController{
    
    let cellName2: String = "listCell2"
    
    @IBOutlet weak var tableview2: UITableView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        tableview2.delegate = self
        tableview2.dataSource = self
    }
    
    
}


extension File: UITableViewDataSource, UITableViewDelegate {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return cellTitle2.count
    }
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 150
    }
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let customCell2 = tableview2.dequeueReusableCell(withIdentifier: cellName2, for: indexPath) as! ListCell2
        customCell2.testimg.image = UIImage(named:String(cellImage2[indexPath.row]))
        customCell2.testlabel1.text = cellTitle2[indexPath.row]
        customCell2.testlabel2.text = cellContent2[indexPath.row]
    
        return customCell2
    }
}
