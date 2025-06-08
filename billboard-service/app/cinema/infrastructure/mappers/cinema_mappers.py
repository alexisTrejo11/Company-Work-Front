from datetime import datetime, timezone
from typing import List
from app.cinema.core.entities.cinema import ( 
    Cinema, CinemaStatus, CinemaType, CinemaFeatures, CinemaAmenities, ContactInfo, Location, SocialMedia
)
from app.cinema.infrastructure.persistence.model.cinema_model import ( 
    CinemaModel, CinemaStatusEnum, CinemaTypeEnum, LocationRegionEnum
)

class CinemaModelMapper:
    @staticmethod
    def from_domain(entity: Cinema) -> CinemaModel:
        """
        Converts a Cinema domain entity to a CinemaModel ORM model.
        """
        if not isinstance(entity, Cinema):
            raise ValueError("Entity must be a Cinema instance")

        features_list_str = [feature for feature in entity.features] if entity.features else []

        return CinemaModel(
            id=entity.id,
            image=entity.image,
            name=entity.name,
            tax_number=entity.tax_number,
            is_active=entity.is_active,
            description=entity.description,
            screens=entity.screens,
            last_renovation=entity.last_renovation,

            type=CinemaTypeEnum[entity.type], 
            status=CinemaStatusEnum[entity.status], 
            region=LocationRegionEnum[entity.region],

            has_parking=entity.amenities.parking,
            has_food_court=entity.amenities.food_court,
            has_coffee_station=entity.amenities.coffee_station,
            has_disabled_access=entity.amenities.disabled_access,

            address=entity.contact_info.address,
            phone=entity.contact_info.phone,
            email_contact=entity.contact_info.email_contact, 

            latitude=entity.location.lat,
            longitude=entity.location.lng,

            facebook_url=entity.social_media.facebook,
            instagram_url=entity.social_media.instagram,
            x_url=entity.social_media.x,
            tik_tok_url=entity.social_media.tik_tok,
            
            features=features_list_str,
            
            created_at= datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

    @staticmethod
    def to_domain(model: CinemaModel) -> Cinema:
        """
        Converts a CinemaModel ORM model to a Cinema domain entity.
        """
        if not isinstance(model, CinemaModel):
            raise ValueError("Model must be a CinemaModel instance")

        features_list_enum = [CinemaFeatures(feature_str) for feature_str in model.features] if model.features else []

        return Cinema(
            id=model.id,
            image=model.image,
            name=model.name,
            tax_number=model.tax_number,
            is_active=model.is_active,
            description=model.description,
            screens=model.screens,
            last_renovation=model.last_renovation,

            type=CinemaType[model.type.value],
            status=CinemaStatus[model.status.value],
            region=LocationRegionEnum[model.region.value],

            amenities=CinemaAmenities(
                parking=model.has_parking,
                food_court=model.has_food_court,
                coffee_station=model.has_coffee_station,
                disabled_access=model.has_disabled_access
            ),

            contact_info=ContactInfo(
                address=model.address,
                phone=model.phone,
                email_contact=model.email_contact,
                location={
                    "lat": model.latitude,
                    "lng": model.longitude
                }
            ),

            location=Location(
                lat=model.latitude,
                lng=model.longitude
            ),

            social_media=SocialMedia(
                facebook=model.facebook_url,
                instagram=model.instagram_url,
                x=model.x_url,
                tik_tok=model.tik_tok_url
            ),

            features=features_list_enum,
        )