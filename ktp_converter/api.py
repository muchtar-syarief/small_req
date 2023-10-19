# import requests
# import re
# import json
# import os

# def sharpen_image(pathfile):
#     client_id = "c5e4f61e1a6c3b1521b541bc5c5a2ac5"
#     license_id = 13031466

#     base_header = {
#         "Accept": "application/json, text/plain, */*",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Accept-Language": "en-US,en;q=0.9",
#         "Authorization": "Bearer v1,201216729,363,bcbf44663262c201ce5a3fc79e1a91d20",
#         "Content-Type": "application/json;charset=UTF-8",
#         "Origin": "https://picwish.com",
#         "Referer": "https://picwish.com/id/unblur-%20image-portrait",
#         "Sec-Ch-Ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
#         "Sec-Ch-Ua-Mobile": "?0",
#         "Sec-Ch-Ua-Platform": '"Windows"',
#         "Sec-Fetch-Dest": "empty",
#         "Sec-Fetch-Mode": "cors",
#         "Sec-Fetch-Site": "cross-site",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
#     }

#     cookies = {
#         "__lc_cid": "84dc1e4a-4bcf-454d-bbf7-4b0d43a9e363",
#         "__lc_cid": "84dc1e4a-4bcf-454d-bbf7-4b0d43a9e363",
#         "__lc_cst": "5e22cacb283763431b894a2424b72b6430ea06bb8e348fbf78da177e8dac4f49e4954487e466058bd9aacddec798cfef687620c694259e3591917675033b","__lc_cst": "5e22cacb283763431b894a2424b72b6430ea06bb8e348fbf78da177e8dac4f49e4954487e466058bd9aacddec798cfef687620c694259e3591917675033b",
#         "__oauth_redirect_detector": "counter=1&t=1697695428&tag=43d3d84b6973b9bbe3063314a93c378b5f3cf860"
#     }
#     session = requests.Session()
#     session.headers = base_header

#     login_payload = {
#         "brand_id":29,
#         "app_id":363,
#         "language":"id",
#         "type":27,
#         "device_hash":"xxxwebdevicehashxxxxxxxxxxxxxxxx",
#         "platform":2,
#         "os_name":"HONOR",
#         "os_version":"9"
#         }
#     login = session.post(url="https://gw.aoscdn.com/base/passport/v1/api/login", data=login_payload, headers=base_header)
#     login_data = login.json()
#     api_token = login_data["data"]["api_token"]
#     device_id = login_data["data"]["device_id"]

#     dyn_conf = session.get(url=f"https://api.livechatinc.com/v3.6/customer/action/get_dynamic_configuration?license_id=13031466&client_id={client_id}&url=https%3A%2F%2Fpicwish.com%2Fid%2Funblur-%2520image-portrait&channel_type=code&jsonp=__qyzw9s7dzl")
#     data_str = dyn_conf.text
#     output_str = re.search(r"\((.+?)\)", data_str, re.DOTALL | re.MULTILINE).group(1)
#     dyn_conf_data = json.loads(output_str)
#     organization_id = dyn_conf_data["organization_id"]

#     session.headers["Content-Type"] = "text/plain;charset=UTF-8"
#     session.headers["Origin"] = "https://secure.livechatinc.com"
#     session.headers["Referer"] = "https://secure.livechatinc.com/"
#     token_payload = {
#         "response_type":"token",
#         "grant_type":"cookie",
#         "client_id": client_id,
#         "organization_id": organization_id,
#         "redirect_uri":"https://secure.livechatinc.com/customer/action/open_chat"
#     }
#     token = session.post(url="https://accounts.livechatinc.com/v2/customer/token", data=token_payload, cookies=cookies)
#     print(token)

#     fname = os.path.split(pathfile)[-1]

#     oss_payload = {
#         "task_type":303,"filenames":["1671100106860008_2.jpg"]
#     }
#     oss = session.post(url="https://gw.aoscdn.com/app/picwish/authorizations/oss", data=oss_payload)
#     oss_data = oss.json()["data"]
#     access_key_id = oss_data["credential"]["access_key_id"]
#     access_key_secret = oss_data["credential"]["access_key_secret"]

#     loc_upload = oss_data["objects"][fname]


#     session.headers["Content-Type"] = "image/jpeg"
#     session.headers["Origin"] = "https://picwish.com"
#     session.headers["Referer"] = "https://picwish.com/id/unblur-%20image-portrait"
#     session.headers["Content-Disposition"] = fname
#     # session.headers["Authorization"] = 


#     upload_uri = f"https://picwishhk.oss-accelerate.aliyuncs.com/{loc_upload}"
#     put_img = session.put(url=upload_uri, files = {'file': open(pathfile, 'rb')})
#     print(put_img)


# if __name__ == "__main__": 
#     sharpen_image("main_images/1671100106860008_2.jpg")



    
    # file = 'output/1671100106860008_2.jpg'
    # ext = os.path.splitext(file)[-1]
    # image = Image.open(file)

    # image_faces = face_recognition.load_image_file(file)
    # faces = face_recognition.face_locations(image_faces)
    # print(len(faces))
    
    
    
    # dst = Image.new('RGB', (image.width, image.height))
    # dst.paste(image, (0, 0))

    # for i in range(len(faces)):
    #     top, right, bottom, left = faces[i]

    #     print(top, right, bottom, left)

    #     face_image = image_faces[top:bottom, left:right]
    #     face = Image.fromarray(face_image)


    #     # final.save("%s%s%s" % (output_file, str(i), ext))
    #     location = (left, top)
    #     dst.paste(face, location)

    # output_file = os.path.join(file.replace(ext, ""))
    # dst.save("%s%s-asd%s" % (output_file, str(i), ext))

            
        # image = Image.open(file)

        # image_faces = face_recognition.load_image_file(file)
        # faces = face_recognition.face_locations(image_faces)
        # print('done')
        # for i in range(len(faces)):
        #     top, right, bottom, left = faces[i]

        #     face_image = image_faces[top:bottom, left:right]
        #     final = Image.fromarray(face_image)

        #     output_file = os.path.join(output, fname.replace(ext, ""))

        #     final.save("%s%s%s" % (output_file, str(i), ext))

        
# def get_concat_h(base_image, second_image, location):
#     dst = Image.new('RGB', (base_image.width, base_image.height))
#     dst.paste(base_image, (0, 0))
#     dst.paste(second_image, location)
#     return dst


# def gfpgan(folder):
#     for fname in get_files(folder):
#         pathfile = os.path.join(folder, fname)
#         result = replicate.run(
#             "tencentarc/gfpgan:9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3",
#             input={"img": open(pathfile, "rb")}
#         )
#         print(result)
