

function get_rand () {
    return Math.random()
}

function get_suid () {
    return Math.round(2147483647 * Math.random()) * (new Date).getUTCMilliseconds() % 1e10
}

function get_uuid () {
    return (new Date).getTime() + "";
}