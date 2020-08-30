from dataclasses import dataclass, asdict
from typing import Dict

from redisgraph import Node, Edge

from app import users_graph


@dataclass
class User:
    """User Model"""

    first_name: str
    last_name: str
    birth_date: str
    zip_code: str

    @property
    def data(self) -> Dict:
        return asdict(self)

    @property
    def label(self) -> str:
        return "user"


def add_user(user: User):
    user_node = Node(label="user", properties=user.data)
    users_graph.add_node(user_node)
    users_graph.commit()


def get_user(user: User):
    params = user.data
    query = """
    MATCH (u:user)
    WHERE u.first_name = '{first_name}'
    AND u.last_name = '{last_name}'
    AND u.birth_date = '{birth_date}'
    AND u.zip_code = '{zip_code}'
    RETURN u
    """.format(
        **user.data
    )
    result = users_graph.query(query, params)
    try:
        user_node = result.result_set[0][0]
        user_node.alias = list(users_graph.nodes.keys())[
            list(users_graph.nodes.values()).index(user_node)
        ]  # Alias isn't returned when getting nodes like this.
    except (IndexError, ValueError):
        user_node = None
    return user_node


def add_friend(user: User, other: User):
    me = get_user(user)
    friend = get_user(other)
    if not friend:
        add_user(friend)
        friend = get_user(friend)
    edge = Edge(me, "friends", friend)
    # check if edge exists create_or_add
    users_graph.add_edge(edge)
    users_graph.commit()


def get_friends(user: User):
    params = user.data
    query = """
    MATCH (u:user)-[f:friends]->(them:user)
    WHERE u.first_name = '{first_name}'
    AND u.last_name = '{last_name}'
    AND u.birth_date = '{birth_date}'
    AND u.zip_code = '{zip_code}'
    RETURN them
    """.format(
        **user.data
    )
    result = users_graph.query(query, params)
    return result.result_set


def reset():
    users_graph.flush()
    users_graph.commit()


joe = User("Joe", "Schmoe", "01/01/1945", "48044")
