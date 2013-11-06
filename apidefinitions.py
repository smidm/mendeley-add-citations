# API method definitions. Used to create MendeleyRemoteMethod instances
methods = {
    ######## Public Resources ########
    'details': {
        'required': ['id'],
        'optional': ['type'],
        'url': '/oapi/documents/details/%(id)s/',
        },
    'categories': {
        'url': '/oapi/documents/categories/',    
        },
    'subcategories': {
        'url': '/oapi/documents/subcategories/%(id)s/',
        'required': ['id'],
        },
    'search': {
        'url': '/oapi/documents/search/%(query)s/',
        'required': ['query'],
        'optional': ['page', 'items'],
        },
    'tagged': {
        'url': '/oapi/documents/tagged/%(tag)s/',
        'required': ['tag'],
        'optional': ['cat', 'subcat', 'page', 'items'],
        },
    'related': {
        'url': '/oapi/documents/related/%(id)s/', 
        'required': ['id'],
        'optional': ['page', 'items'],
        },
    'authored': {
        'url': '/oapi/documents/authored/%(author)s/',
        'required': ['author'],
        'optional': ['page', 'items'],
        },
    'public_groups': {
        'url': '/oapi/documents/groups/',
        'optional': ['page', 'items', 'cat']
        },
    'public_group_details': {
        'url': '/oapi/documents/groups/%(id)s/',
        'required': ['id'],
        },
    'public_group_docs': {
        'url': '/oapi/documents/groups/%(id)s/docs/',
        'required': ['id'],
        'optional': ['details', 'page', 'items'],
        },
    'public_group_people': {
        'url': '/oapi/documents/groups/%(id)s/people/',
        'required': ['id'],
        },
    'author_stats': {
        'url': '/oapi/stats/authors/',
        'optional': ['discipline', 'upandcoming'],
        },
    'paper_stats': {
        'url': '/oapi/stats/papers/',
        'optional': ['discipline', 'upandcoming'],
        },
    'publication_stats': {
        'url': '/oapi/stats/publications/',
        'optional': ['discipline', 'upandcoming'],
        },
    'tag_stats': {
        'url': '/oapi/stats/tags/%(discipline)s/',
        'required': ['discipline'],
        'optional': ['upandcoming'],
        },
    ######## User Specific Resources ########
    'library_author_stats': {
        'url': '/oapi/library/authors/',
        'access_token_required': True,
        },
    'library_tag_stats': {
        'url': '/oapi/library/tags/',
        'access_token_required': True,
        },
    'library_publication_stats': {
        'url': '/oapi/library/publications/',
        'access_token_required': True,
        },
    'library': {
        'url': '/oapi/library/',
        'optional': ['page', 'items'],
        'access_token_required': True,
        },
    'create_document': {
        'url': '/oapi/library/documents/',
        # HACK: 'document' is required, but by making it optional here it'll get POSTed
        # Unfortunately that means it needs to be a named param when calling this method
        'optional': ['document'],
        'access_token_required': True,
        'method': 'post',
        },
    'create_document_from_canonical': {
        'url': '/oapi/library/documents/',
        'optional': ['canonical_id'],
        'access_token_required': True,
        'method': 'post',
        },
    'update_document': {
        'url': '/oapi/library/documents/%(id)s',
        'required': ['id'],
        # HACK: 'document' is required, but by making it optional here it'll get POSTed
        # Unfortunately that means it needs to be a named param when calling this method
        'optional': ['document'],
        'access_token_required': True,
        'method': 'post',
        },
    '_upload_pdf': {
        'url': '/oapi/library/documents/%(id)s/',
        'required': ['id'],
        'optional': ['data', 'file_name', 'oauth_body_hash', 'sha1_hash'],
        'access_token_required': True,
        'method': 'put'
	},
    'download_file': {
        'url': '/oapi/library/documents/%(id)s/file/%(hash)s/',
        'required': ['id', 'hash'],
        'optional' : ['with_redirect'],
        'access_token_required': True,
        'method': 'get'
        },
    'download_file_group': {
        'url': '/oapi/library/documents/%(id)s/file/%(hash)s/%(group)s/',
        'required': ['id', 'hash', 'group'],
        'optional' : ['with_redirect'],
        'access_token_required': True,
        'method': 'get'
        },
    'document_details': {
        'url': '/oapi/library/documents/%(id)s/',
        'required': ['id'],
        'access_token_required': True,
        },
    'documents_authored': {
        'url': '/oapi/library/documents/authored/',
        'access_token_required': True,
        },
    'documents_starred': {
        'url': '/oapi/library/documents/starred/',
        'access_token_required': True,
    },
    'delete_library_document': {
        'url': '/oapi/library/documents/%(id)s/',
        'required': ['id'],
        'access_token_required': True,
        'method': 'delete',
        'expected_status':204,
        },
    'contacts': {
        'url': '/oapi/profiles/contacts/',
        'access_token_required': True,
        'method': 'get',    
        }, 
    'contacts_of_contact': {
        'url': '/oapi/profiles/contacts/%(id)s/', 
        'required': ['id'],
        'access_token_required': True, 
        'method': 'get',
        },
    'add_contact': {
        'url': '/oapi/profiles/contacts/%(id)s/',
        'required': ['id'],
        'access_token_required': True,
        'method': 'post',
        },
    # Folders methods #
    'folders': {
        'url': '/oapi/library/folders/',
        'access_token_required': True,
        },
    'folder_documents': {
        'url': '/oapi/library/folders/%(id)s/',
        'required': ['id'],
        'optional': ['page', 'items'],
        'access_token_required': True,
        },
    'create_folder': {
        'url': '/oapi/library/folders/',
        # HACK: 'folder' is required, but by making it optional here it'll get POSTed
        # Unfortunately that means it needs to be a named param when calling this method
        'optional': ['folder'],
        'access_token_required': True,
        'method': 'post',
        },
    'delete_folder': {
        'url': '/oapi/library/folders/%(id)s/',
        'required': ['id'],
        'access_token_required': True,
        'method': 'delete',
        'expected_status':204,
        },
    'add_document_to_folder': {
        'url': '/oapi/library/folders/%(folder_id)s/%(document_id)s/',
        'required': ['folder_id', 'document_id'],
        'access_token_required': True,
        'method': 'post',
        },
    'delete_document_from_folder': {
        'url': '/oapi/library/folders/%(folder_id)s/%(document_id)s/',
        'required': ['folder_id', 'document_id'],
        'access_token_required': True,
        'method': 'delete',
        'expected_status':204,
        },
    # Groups methods #
    'groups': {
        'url': '/oapi/library/groups/',
        'access_token_required': True,
        },
    'group_documents': {
        'url': '/oapi/library/groups/%(id)s/',
        'required': ['id'],
        'optional': ['page', 'items'],
        'access_token_required': True,
        },
    'group_doc_details': {
        'url': '/oapi/library/groups/%(group_id)s/%(doc_id)s/',
        'required': ['group_id', 'doc_id'],
        'access_token_required': True,
        },
    'group_people': {
        'url': '/oapi/library/groups/%(id)s/people/', 
        'required': ['id'],
        'access_token_required': True,
        },        
    'create_group': {
        'url': '/oapi/library/groups/',
        'optional': ['group'],
        'access_token_required': True,
        'method': 'post',
        },
    'delete_group': {
        'url': '/oapi/library/groups/%(id)s/',
        'required': ['id'],
        'access_token_required': True,
        'method': 'delete',
        'expected_status':204,
        },
    'leave_group': {
        'url': '/oapi/library/groups/%(id)s/leave/', 
        'required': ['id'],
        'access_token_required': True, 
        'method': 'delete',
        },
    'unfollow_group': {
        'url': '/oapi/library/groups/%(id)s/unfollow/', 
        'required': ['id'],
        'access_token_required': True, 
        'method': 'delete',
        },
    'delete_group_document': {
        'url': '/oapi/library/groups/%(group_id)s/%(document_id)s/',
        'required': ['group_id', 'document_id'],
        'access_token_required': True,
        'method': 'delete',
        'expected_status':204,
        },
    # Group Folders methods #
    'group_folders': {
        'url': '/oapi/library/groups/%(group_id)s/folders/',
        'required': ['group_id'],
        'access_token_required': True,
        },
    'group_folder_documents': {
        'url': '/oapi/library/groups/%(group_id)s/folders/%(id)s/',
        'required': ['group_id', 'id'],
        'optional': ['page', 'items'],
        'access_token_required': True,
        },
    'create_group_folder': {
        'url': '/oapi/library/groups/%(group_id)s/folders/',
        'required': ['group_id'],
        # HACK: 'folder' is required, but by making it optional here it'll get POSTed
        # Unfortunately that means it needs to be a named param when calling this method
        'optional': ['folder'],
        'access_token_required': True,
        'method': 'post',
        },
    'delete_group_folder': {
        'url': '/oapi/library/groups/%(group_id)s/folders/%(id)s/',
        'required': ['group_id', 'id'],
        'access_token_required': True,
        'method': 'delete',
        'expected_status':204,
        },
    'add_document_to_group_folder': {
        'url': '/oapi/library/groups/%(group_id)s/folders/%(folder_id)s/%(document_id)s/',
        'required': ['group_id', 'folder_id', 'document_id'],
        'access_token_required': True,
        'method': 'post',
        },
    'delete_document_from_group_folder': {
        'url': '/oapi/library/groups/%(group_id)s/folders/%(folder_id)s/%(document_id)s/',
        'required': ['group_id', 'folder_id', 'document_id'],
        'access_token_required': True,
        'method': 'delete',
        'expected_status':204,
        },
    'profile_info': {
        'url': '/oapi/profiles/info/%(id)s/',
        'required': ['id'],
        'access_token_required': True,
        'method': 'get',    
        }, 

    'my_profile_info': {
        'url': '/oapi/profiles/info/me/',
        'access_token_required': True,
        'method': 'get'
        },
    }
