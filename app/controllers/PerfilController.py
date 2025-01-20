from app.models.tables import User, Perfil
from app.ext.db import db

class PerfilController():

    @staticmethod
    def allow_user(allowed, user_id):
        user = User.query.filter_by(_id=user_id).first()
        user.allow = allowed
        db.session.commit()
    
    @staticmethod
    def is_allowed(user_id):
        return User.query.filter_by(_id=user_id).first().allow
    
    @staticmethod
    def is_admin(user_id):
        return User.query.filter_by(_id=user_id).first().admin
    
    @staticmethod
    def set_permissions(data):
        perfil = Perfil.query.filter_by(_id=data["perf_id"]).first()
        perfil.create_filter = True if data["can_create_filter"] == "S" else False
        perfil.create_dados = True if data["can_create_dados"] == "S" else False
        perfil.view_users = True if data["can_view_users"] == "S" else False
        perfil.view_perfis = True if data["can_view_perfis"] == "S" else False
        db.session.commit()

    @staticmethod
    def get_permission_from_p_id(perm_id):
        return Perfil.query.filter_by(_id=perm_id).first()
    
    @staticmethod
    def get_permission_object(user_id):
        user = User.query.filter_by(_id=user_id).first()
        permission =  Perfil.query.filter_by(nome=user.dep).first()
        return permission

    @staticmethod
    def can_create_filter(user_id):
        permission = PerfilController.get_permission_object(user_id)
        return (permission.create_filter and PerfilController.is_allowed(user_id)) or PerfilController.is_admin(user_id)
    
    @staticmethod
    def can_create_dados(user_id):
        permission = PerfilController.get_permission_object(user_id)
        return (permission.create_dados and PerfilController.is_allowed(user_id)) or PerfilController.is_admin(user_id)
    
    @staticmethod
    def can_view_users(user_id):
        permission = PerfilController.get_permission_object(user_id)
        return (permission.view_users and PerfilController.is_allowed(user_id)) or PerfilController.is_admin(user_id)

    @staticmethod
    def can_view_perfis(user_id):
        permission = PerfilController.get_permission_object(user_id)
        return (permission.view_perfis and PerfilController.is_allowed(user_id)) or PerfilController.is_admin(user_id)

    @staticmethod
    def get_from_user(user_id):
        permission = PerfilController.get_permission_object(user_id)
        return permission 

    @staticmethod
    def get_all():
        permissions =  Perfil.query.all()
        return permissions

