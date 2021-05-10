//
//  Community.swift
//  HairStylePreview
//
//  Created by 김정태 on 2021/04/05.
//
//community

import UIKit

var cellImage = ["6","1"]
var cellTitle: Array<String> = ["ID 1","ID 2"]
var cellContent: Array<String> = ["어때요?","괜찮나요?"]

class Community: UIViewController{
    
    @IBOutlet weak var tableview_custom: UITableView!
    let cellName: String = "listCell"
    
    override func viewDidLoad() {
        super.viewDidLoad()
        tableview_custom.delegate = self
        tableview_custom.dataSource = self
        //tableview_custom.rowHeight = UITableView.automaticDimension
        //tableview_custom.estimatedRowHeight = 500
        
    }
    @IBAction func communityBtnAdd(_ sender: UIBarButtonItem) {
        if let controller = self.storyboard?.instantiateViewController(identifier: "CommunityAdd") {
            self.navigationController?.pushViewController(controller, animated: true)
        }
    }
    
}


extension Community: UITableViewDataSource, UITableViewDelegate {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return cellTitle.count
    }
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 150
    }
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let customCell = tableview_custom.dequeueReusableCell(withIdentifier: cellName, for: indexPath) as! ListCell
        customCell.communityImage.image = UIImage(named:String(cellImage[indexPath.row]))
        customCell.communityID.text = cellTitle[indexPath.row]
        customCell.communityContent.text = cellContent[indexPath.row]
    
        return customCell
    }
}
