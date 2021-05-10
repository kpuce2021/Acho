//
//  ListCell2.swift
//  HairStylePreview
//
//  Created by 김정태 on 2021/05/10.
//

import UIKit

class ListCell2: UITableViewCell {

    @IBOutlet weak var testimg: UIImageView!
    
    @IBOutlet weak var testlabel1: UILabel!
    
    @IBOutlet weak var testlabel2: UILabel!
    
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
