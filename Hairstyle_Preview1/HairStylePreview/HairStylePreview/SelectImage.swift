//
//  SelectImage.swift
//  HairStylePreview
//
//  Created by 곽재선 on 2021/05/07.
//

import UIKit

struct ImageInfo {
    let name: String
    
    var image: UIImage? {
        return UIImage(named: "\(name).png")
    }
    
    init (name: String) {
        self.name = name
    }
}

class SelectImage: UIViewController,UICollectionViewDataSource, UICollectionViewDelegate {
    
    let viewModel = ImageViewModel()
    
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return viewModel.countOfImageList
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        guard let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "cell", for: indexPath) as? Cell else {
                return UICollectionViewCell()
            }
        let imageInfo = viewModel.imageInfo(at: indexPath.item)
        cell.update(info: imageInfo)
        return cell
    }
    
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        
        let vcName = self.storyboard?.instantiateViewController(withIdentifier: "Result")
        vcName?.modalTransitionStyle = .coverVertical
        self.present(vcName!, animated: true, completion: nil)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
    }
}
class Cell: UICollectionViewCell {
    @IBOutlet weak var imgView: UIImageView!
    
    func update(info: ImageInfo) {
            imgView.image = info.image
        }
}

class ImageViewModel {
    let imageInfoList: [ImageInfo] = [
        ImageInfo(name: "1"),
        ImageInfo(name: "3"),
        ImageInfo(name: "4"),
        ImageInfo(name: "6"),
        ImageInfo(name: "7"),
        ImageInfo(name: "8"),
    ]
    
    var countOfImageList: Int {
        return imageInfoList.count
    }
    
    func imageInfo(at index: Int) -> ImageInfo {
        return imageInfoList[index]
    }
}
