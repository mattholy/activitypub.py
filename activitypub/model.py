from pydantic import BaseModel, Field, HttpUrl
from pydantic import field_validator
from datetime import datetime
from typing import Optional, Union, List, Dict, Any, Literal


class ActivityStreamsBase(BaseModel):
    activitypub_context: Optional[
        Union[HttpUrl, List[Union[HttpUrl, Dict[str, Any]]]]
    ] = Field(None, alias='@context')
    id: Optional[HttpUrl] = Field(None, alias='id')
    type: Optional[str] = Field(None, alias='type')

    @field_validator('activitypub_context')
    def validate_context(cls, value):
        if (
            isinstance(value, str)
            and 'https://www.w3.org/ns/activitystreams' not in value
        ):
            raise ValueError(
                '@context must include "https: // www.w3.org/ns/activitystreams".'
            )
        if (
            isinstance(value, list)
            and 'https://www.w3.org/ns/activitystreams' not in value
        ):
            raise ValueError(
                '@context must include "https: // www.w3.org/ns/activitystreams".'
            )
        return value

    class Config:
        populate_by_name = True


class BaseObject(ActivityStreamsBase):
    type: str = Field(None, alias='type')

    attachment: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = Field(
        None, alias='attachment'
    )
    attributed_to: Optional[Union[str, List[str]]
                            ] = Field(None, alias='attributedTo')
    audience: Optional[Union[str, List[str]]] = Field(None, alias='audience')
    content: Optional[str] = Field(None, alias='content')
    context: Optional[Union[str, Dict[str, Any]]
                      ] = Field(None, alias='context')
    name: Optional[str] = Field(None, alias='name')
    end_time: Optional[datetime] = Field(None, alias='endTime')
    generator: Optional[str] = Field(None, alias='generator')
    icon: Optional[Union[str, Dict[str, Any]]] = Field(None, alias='icon')
    image: Optional[Union[str, Dict[str, Any]]] = Field(None, alias='image')
    in_reply_to: Optional[str] = Field(None, alias='inReplyTo')
    location: Optional[Union[str, Dict[str, Any]]
                       ] = Field(None, alias='location')
    preview: Optional[Union[str, Dict[str, Any]]
                      ] = Field(None, alias='preview')
    published: Optional[datetime] = Field(None, alias='published')
    replies: Optional[Union[str, Dict[str, Any]]
                      ] = Field(None, alias='replies')
    start_time: Optional[datetime] = Field(None, alias='startTime')
    summary: Optional[str] = Field(None, alias='summary')
    tag: Optional[Union[str, List[str]]] = Field(None, alias='tag')
    updated: Optional[datetime] = Field(None, alias='updated')
    url: Optional[str] = Field(None, alias='url')
    to: Optional[Union[str, List[str]]] = Field(None, alias='to')
    bto: Optional[Union[str, List[str]]] = Field(None, alias='bto')
    cc: Optional[Union[str, List[str]]] = Field(None, alias='cc')
    bcc: Optional[Union[str, List[str]]] = Field(None, alias='bcc')
    media_type: Optional[str] = Field(None, alias='mediaType')
    duration: Optional[str] = Field(None, alias='duration')


class BaseLink(ActivityStreamsBase):
    href: HttpUrl = Field(None, alias='href')
    rel: Optional[str] = Field(None, alias='rel')
    media_type: Optional[str] = Field(None, alias='mediaType')
    name: Optional[str] = Field(None, alias='name')
    hreflang: Optional[str] = Field(None, alias='hreflang')
    height: Optional[int] = Field(None, alias='height')
    width: Optional[int] = Field(None, alias='width')
    preview: Optional[HttpUrl] = Field(None, alias='preview')


class BaseActivity(BaseObject):
    type: Literal[
        'Accept', 'Add', 'Announce', 'Arrive', 'Block', 'Create', 'Delete',
        'Dislike', 'Flag', 'Follow', 'Ignore', 'Invite', 'Join', 'Leave',
        'Like', 'Listen', 'Move', 'Offer', 'Question', 'Reject', 'Read',
        'Remove', 'TentativeReject', 'TentativeAccept', 'Travel', 'Undo',
        'Update', 'View'
    ] = Field(None, alias='type')
    actor: Union[HttpUrl, 'Actor'] = Field(None, alias='actor')
    object: Optional[Union[HttpUrl, BaseObject]] = Field(None, alias='object')
    target: Optional[Union[HttpUrl, BaseObject]] = Field(None, alias='target')
    result: Optional[Union[HttpUrl, BaseObject]] = Field(None, alias='result')
    origin: Optional[Union[HttpUrl, BaseObject]] = Field(None, alias='origin')
    instrument: Optional[Union[HttpUrl, BaseObject]
                         ] = Field(None, alias='instrument')


class IntransitiveActivity(BaseActivity):
    object: None = Field(None, alias='object')


class BaseCollection(BaseObject):
    type: str = 'Collection'
    total_items: Optional[int] = Field(None, alias='totalItems')
    current: Optional[Union[HttpUrl, BaseObject]
                      ] = Field(None, alias='current')
    first: Optional[Union[HttpUrl, BaseObject]] = Field(None, alias='first')
    last: Optional[Union[HttpUrl, BaseObject]] = Field(None, alias='last')
    items: Optional[List[Union[HttpUrl, BaseObject]]
                    ] = Field(None, alias='items')


class OrderedCollection(BaseCollection):
    type: str = 'OrderedCollection'


class CollectionPage(BaseCollection):
    part_of: Optional[Union[HttpUrl, BaseCollection]
                      ] = Field(None, alias='partOf')
    next: Optional[Union[HttpUrl, BaseCollection]] = Field(None, alias='next')
    prev: Optional[Union[HttpUrl, BaseCollection]] = Field(None, alias='prev')


class OrderedCollectionPage(CollectionPage):
    type: str = 'OrderedCollectionPage'


class Actor(ActivityStreamsBase):
    type: str = Field(None, alias='type')
    inbox: HttpUrl = Field(None, alias='inbox')
    outbox: HttpUrl = Field(None, alias='outbox')
    following: Optional[HttpUrl] = Field(None, alias='following')
    followers: Optional[HttpUrl] = Field(None, alias='followers')
    liked: Optional[HttpUrl] = Field(None, alias='liked')
    streams: Optional[List[HttpUrl]] = Field(None, alias='streams')
    preferred_username: Optional[str] = Field(None, alias='preferredUsername')
    endpoints: Optional[Dict[str, HttpUrl]] = Field(None, alias='endpoints')
    proxy_url: Optional[HttpUrl] = Field(None, alias='proxyUrl')
    oauth_authorization_endpoint: Optional[HttpUrl] = Field(
        None, alias='oauthAuthorizationEndpoint')
    oauth_token_endpoint: Optional[HttpUrl] = Field(
        None, alias='oauthTokenEndpoint')
    provide_client_key: Optional[HttpUrl] = Field(
        None, alias='provideClientKey')
    sign_client_key: Optional[HttpUrl] = Field(None, alias='signClientKey')
    shared_inbox: Optional[HttpUrl] = Field(None, alias='sharedInbox')

# =================================================================================================
# Activity Types
# =================================================================================================


class AcceptActivity(BaseActivity):
    type: str = Field('Accept')


class AddActivity(BaseActivity):
    type: str = Field('Add')


class AnnounceActivity(BaseActivity):
    type: str = Field('Announce')


class ArriveActivity(IntransitiveActivity):
    type: str = Field('Arrive')


class CreateActivity(BaseActivity):
    type: str = Field('Create')


class DeleteActivity(BaseActivity):
    type: str = Field('Delete')


class DislikeActivity(BaseActivity):
    type: str = Field('Dislike')


class FlagActivity(BaseActivity):
    type: str = Field('Flag')


class FollowActivity(BaseActivity):
    type: str = Field('Follow')


class IgnoreActivity(BaseActivity):
    type: str = Field('Ignore')


class BlockActivity(IgnoreActivity):
    type: str = Field('Block')


class JoinActivity(BaseActivity):
    type: str = Field('Join')


class LeaveActivity(BaseActivity):
    type: str = Field('Leave')


class LikeActivity(BaseActivity):
    type: str = Field('Like')


class ListenActivity(BaseActivity):
    type: str = Field('Listen')


class MoveActivity(BaseActivity):
    type: str = Field('Move')


class OfferActivity(BaseActivity):
    type: str = Field('Offer')


class InviteActivity(OfferActivity):
    type: str = Field('Invite')


class QuestionActivity(IntransitiveActivity):
    type: str = Field('Question')
    one_of: Optional[List[BaseObject]] = Field(None, alias='oneOf')
    any_of: Optional[List[BaseObject]] = Field(None, alias='anyOf')
    closed: Optional[datetime] = Field(None, alias='closed')


class RejectActivity(BaseActivity):
    type: str = Field('Reject')


class ReadActivity(BaseActivity):
    type: str = Field('Read')


class RemoveActivity(BaseActivity):
    type: str = Field('Remove')


class TentativeRejectActivity(RejectActivity):
    type: str = Field('TentativeReject')


class TentativeAcceptActivity(AcceptActivity):
    type: str = Field('TentativeAccept')


class TravelActivity(IntransitiveActivity):
    type: str = Field('Travel')


class UndoActivity(BaseActivity):
    type: str = Field('Undo')


class UpdateActivity(BaseActivity):
    type: str = Field('Update')


class ViewActivity(BaseActivity):
    type: str = Field('View')

# =================================================================================================
# Actor Types
# =================================================================================================


class ApplicationActor(Actor):
    type: str = Field('Application')


class GroupActor(Actor):
    type: str = Field('Group')


class OrganizationActor(Actor):
    type: str = Field('Organization')


class PersonActor(Actor):
    type: str = Field('Person')


class ServiceActor(Actor):
    type: str = Field('Service')

# =================================================================================================
# Object Types
# =================================================================================================


class ArticleObject(BaseObject):
    type: str = Field('Article')


class DocumentObject(BaseObject):
    type: str = Field('Document')


class AudioObject(DocumentObject):
    type: str = Field('Audio')


class EventObject(BaseObject):
    type: str = Field('Event')


class ImageObject(DocumentObject):
    type: str = Field('Image')


class NoteObject(BaseObject):
    type: str = Field('Note')


class PageObject(DocumentObject):
    type: str = Field('Page')


class PlaceObject(BaseObject):
    type: str = Field('Place')
    accuracy: Optional[float] = Field(None, alias='accuracy', ge=0, le=100)
    altitude: Optional[float] = Field(None, alias='altitude')
    latitude: Optional[float] = Field(None, alias='latitude')
    longitude: Optional[float] = Field(None, alias='longitude')
    radius: Optional[float] = Field(None, alias='radius', ge=0)
    units: Union[HttpUrl, Literal['cm', 'feet', 'inches',
                                  'km', 'm', 'miles']] = Field('m', alias='units')


class ProfileObject(BaseObject):
    type: str = Field('Profile')


class RelationshipObject(BaseObject):
    type: str = Field('Relationship')
    subject: Union[HttpUrl, BaseObject] = Field(None, alias='subject')
    object: Union[HttpUrl, BaseObject] = Field(None, alias='object')
    relationship: Optional[str] = Field(None, alias='relationship')


class TombstoneObject(BaseObject):
    type: str = Field('Tombstone')
    former_type: str = Field(None, alias='formerType')
    deleted: datetime = Field(None, alias='deleted')


class VideoObject(DocumentObject):
    type: str = Field('Video')

# =================================================================================================
# Link Types
# =================================================================================================


class MentionLink(BaseLink):
    type: str = Field('Mention')
