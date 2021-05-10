//
//  ListCell.swift
//  HairStylePreview
//
//  Created by 곽재선 on 2021/05/10.
//

import UIKit

class ListCell: UITableViewCell {

    @IBOutlet weak var communityImage: UIImageView!
    @IBOutlet weak var communityID: UILabel!
    @IBOutlet weak var communityContent: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
