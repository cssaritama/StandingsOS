export default function StandingsTable({ standings }) {
  if (!standings.length) {
    return <p className="empty">No standings yet. Add teams and record a result.</p>;
  }

  return (
    <div className="table-wrap">
      <table className="standings">
        <thead>
          <tr>
            <th>#</th>
            <th className="team">Team</th>
            <th>Pl</th>
            <th>W</th>
            <th>D</th>
            <th>L</th>
            <th>GD</th>
            <th>Pts</th>
          </tr>
        </thead>
        <tbody>
          {standings.map((row) => (
            <tr key={row.team} className={row.position === 1 && row.played ? "leader" : ""}>
              <td>{row.position}</td>
              <td className="team">{row.team}</td>
              <td>{row.played}</td>
              <td>{row.won}</td>
              <td>{row.drawn}</td>
              <td>{row.lost}</td>
              <td>{row.goal_difference > 0 ? `+${row.goal_difference}` : row.goal_difference}</td>
              <td className="points">{row.points}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
