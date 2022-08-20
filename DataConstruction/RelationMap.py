from Django.ToTheGreatOutDoors.core.management.commands.ConstructData import ConstructData

from pathlib import Path

if __name__ == '__main__':
    # Create the relation map, will take a fairly long time. Recommend you just use the RelationMap.Txt.
    exceptions = ['Religious Grounds', 'Allotments Or Community Growing Spaces', 'Cemetery']
    constructor = ConstructData(Path(Path(__file__).parent.parent, 'env.yaml'), exceptions)

    # Uncomment to run the relation mapping
    # constructor.relation_map()

