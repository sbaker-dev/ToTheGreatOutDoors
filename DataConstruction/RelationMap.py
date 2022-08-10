from DataConstruction.ConstructData import ConstructData


if __name__ == '__main__':
    # Create the relation map, will take a fairly long time. Recommend you just use the RelationMap.Txt.
    exceptions = ['Religious Grounds', 'Allotments Or Community Growing Spaces', 'Cemetery']
    constructor = ConstructData(2000, exceptions)

