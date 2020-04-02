# docker-entrypoint.sh

rootAuthDatabase='admin'
"${mongo[@]}" "$rootAuthDatabase" <<-JS
db.createUser({
    user: $(jq --arg 'user' "$MONGO_USER" --null-input '$user'),
    pwd: $(jq --arg 'pwd' "$MONGO_PASS" --null-input '$pwd'),
    roles: [
        { role: 'root', db: $(jq --arg 'db' "$rootAuthDatabase" --null-input '$db') },
        { role: 'dbOwner', db: $(jq --arg 'db' "$MONGO_DB" --null-input '$db') }
    ]
})

use $MONGO_DB
db.deleteme.save({ deleteme: true })
JS
