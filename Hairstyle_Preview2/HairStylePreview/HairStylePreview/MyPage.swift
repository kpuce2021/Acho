//
//  MyPage.swift
//  HairStylePreview
//
//  Created by 김정태 on 2021/04/28. 
//

import UIKit

class MyPage: UIViewController,UITableViewDataSource,UITableViewDelegate{
    
    
    @IBOutlet var MyPageTable: UITableView!
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 10
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = UITableViewCell.init(style: .default, reuseIdentifier: "TablecellType1")
        
        
        
        return cell
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        MyPageTable.delegate = self
        MyPageTable.dataSource = self
    }
}
