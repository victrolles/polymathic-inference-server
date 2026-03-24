import torch
from aion.modalities import (
    LegacySurveyImage,
    LegacySurveyFluxG,
    LegacySurveyFluxR,
    LegacySurveyFluxI,
    LegacySurveyFluxZ,
    Z
)

def to_tensor(data_array, dtype=torch.float32, device="cuda"):
        return torch.tensor(data_array, dtype=dtype, device=device)

def prepare_all_queries(subset, codec_manager):
    flux_image = []
    for data in subset['image']:
        flux_image.append(data['flux'])

    # Create image modality
    image = LegacySurveyImage(
        flux=to_tensor(flux_image),
        bands=["DES-G", "DES-R", "DES-I", "DES-Z"]
    )

    # Create flux modalities
    g = LegacySurveyFluxG(value=to_tensor(subset['FLUX_G']))
    r = LegacySurveyFluxR(value=to_tensor(subset['FLUX_R']))
    i = LegacySurveyFluxI(value=to_tensor(subset['FLUX_I']))
    z = LegacySurveyFluxZ(value=to_tensor(subset['FLUX_Z']))

    return codec_manager.encode(image, g, r, i, z)

def prepare_query(data, codec_manager):

    # Create image modality
    image = LegacySurveyImage(
        flux=to_tensor(data['image']['flux']).unsqueeze(0),
        bands=["DES-G", "DES-R", "DES-I", "DES-Z"]
    )

    # Create flux modalities
    g = LegacySurveyFluxG(value=to_tensor(data['FLUX_G']).unsqueeze(0))
    r = LegacySurveyFluxR(value=to_tensor(data['FLUX_R']).unsqueeze(0))
    i = LegacySurveyFluxI(value=to_tensor(data['FLUX_I']).unsqueeze(0))
    z = LegacySurveyFluxZ(value=to_tensor(data['FLUX_Z']).unsqueeze(0))

    return codec_manager.encode(image, g, r, i, z)
    
def find_object_in_subset(subset, object_id: str):
    for idx, object_id2 in enumerate(subset['object_id']):
        if object_id == object_id2:
            return idx
    raise ValueError(f"Object {object_id} not found in subset")

def prepare_queries(subset, codec_manager, object_ids):
    flux_image = []
    flux_g = []
    flux_r = []
    flux_i = []
    flux_z = []
    new_object_ids = []
    for i in range(len(subset)):
        if subset[i]['object_id'] in object_ids:
            flux_image.append(subset[i]['image']['flux'])
            flux_g.append(subset[i]['FLUX_G'])
            flux_r.append(subset[i]['FLUX_R'])
            flux_i.append(subset[i]['FLUX_I'])
            flux_z.append(subset[i]['FLUX_Z'])
            new_object_ids.append(subset[i]['object_id'])
    # Create image modality
    image = LegacySurveyImage(
        flux=to_tensor(flux_image),
        bands=["DES-G", "DES-R", "DES-I", "DES-Z"]
    )

    # Create flux modalities
    g = LegacySurveyFluxG(value=to_tensor(flux_g))
    r = LegacySurveyFluxR(value=to_tensor(flux_r))
    i = LegacySurveyFluxI(value=to_tensor(flux_i))
    z = LegacySurveyFluxZ(value=to_tensor(flux_z))

    return codec_manager.encode(image, g, r, i, z), new_object_ids