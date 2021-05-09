//
//  MainMyPage.swift
//  Table
//
//  Created by 김정태 on 2021/05/09.
//  Copyright © 2021 bglee. All rights reserved.
//

import UIKit

class MainMyPage : UIViewController,UICollectionViewDelegate,UICollectionViewDataSource {
    
    let images = ["1","2","3","4","8","7","6"]
    var myimage = ["myImage.png"]
    
    let sectionInsets = UIEdgeInsets(top: 10, left: 10, bottom: 10, right: 10)
    
    @IBOutlet var MyImage: UIImageView!
    
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {

        return images.count
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "RowCell", for: indexPath) as! CustomCell
        
        cell.imgView.image = UIImage(named:String(images[indexPath.row]))

        return cell
    }
    /*
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
        let itemSpacing: CGFloat = 2
        let textAreaHeight: CGFloat = 3
        
        let width: CGFloat = (collectionView.bounds.width - itemSpacing) / 2
        let height: CGFloat = width * 10/7 + textAreaHeight
        return CGSize(width: width, height: height)
        }
    */
    override func viewDidLoad() {
        super.viewDidLoad()
        
        MyImage.image = UIImage(named: String(myimage[0]))
    }

}

class CustomCell : UICollectionViewCell {
    
    @IBOutlet weak var imgView: UIImageView!
}
